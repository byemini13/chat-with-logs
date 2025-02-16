import boto3
import time
import json
from datetime import datetime, timezone

client = boto3.client("logs")


def get_logs_with_context(log_group, start_time, end_time, error_message, log_stream, limit=5, max_occurrences=3):
    """Fetch logs from AWS CloudWatch, including 5 logs before & after each error occurrence."""

    # ✅ Ensure start_time and end_time are always Unix timestamps (int)
    if isinstance(start_time, datetime):
        start_time = int(start_time.timestamp())
    if isinstance(end_time, datetime):
        end_time = int(end_time.timestamp())

    # ✅ Debugging log to confirm the timestamps before making the query
    print(f"🛠️ Debugging AWS Query:")
    print(f"   Log Group: {log_group}")
    print(f"   Log Stream: {log_stream}")
    print(f"   Start Timestamp (Unix): {start_time} → {datetime.utcfromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"   End Timestamp (Unix): {end_time} → {datetime.utcfromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        # ✅ Construct the query
        query_string = f'''
            fields @timestamp, @message
            | filter @logStream like "{log_stream}"
            | sort @timestamp asc
        '''
        
        print(f"📜 Running AWS Query: {query_string.strip()}")

        response = client.start_query(
            logGroupName=log_group,
            startTime=start_time,  # Ensure Unix timestamp
            endTime=end_time,      # Ensure Unix timestamp
            queryString=query_string,
        )
    except Exception as e:
        print(f"❌ AWS CloudWatch Query Failed: {e}")
        return []
    
    query_id = response["queryId"]

    # ✅ Wait for query results
    while True:
        result = client.get_query_results(queryId=query_id)
        if result["status"] in ["Complete", "Failed", "Cancelled"]:
            break
        time.sleep(2)

    # ✅ Debugging: Print raw AWS CloudWatch response
    #print(f"📜 AWS Query Result: {result}")

    # Step 2: Parse logs & extract relevant messages
    all_logs = []
    for row in result.get("results", []):
        raw_log = row[1]["value"]  # Extract @message field
        try:
            log_data = json.loads(raw_log)  # Parse JSON log
            all_logs.append({
                "timestamp": log_data["time"],
                "log": log_data["log"]
            })
        except (json.JSONDecodeError, KeyError):
            continue  # Skip malformed logs

    # Step 3: Find all occurrences of the error
    error_indices = [i for i, log in enumerate(all_logs) if error_message in log["log"]]

    if not error_indices:
        print("❌ No logs found matching the error message.")
        return []

    print(f"🔍 Found {len(error_indices)} occurrences of the error message.")

    # Step 4: Retrieve logs within ±5 range of each error (limit occurrences if needed)
    logs_with_context = []
    for index, error_index in enumerate(error_indices[:max_occurrences]):  # Limit occurrences
        start_index = max(0, error_index - 5)
        end_index = min(len(all_logs), error_index + 6)  # +6 to include the error itself

        context_logs = all_logs[start_index:end_index]
        formatted_logs = [f"{log['timestamp']} - {log['log']}" for log in context_logs]

        logs_with_context.append(f"\n🛑 **Context around Error Occurrence {index + 1}**:")
        logs_with_context.extend(formatted_logs)

    return logs_with_context




# If running as a standalone script
if __name__ == "__main__":
    log_group = "/aws/containerinsights/nonprod/application"

    # ✅ Set start & end time in UTC
    start = datetime(2025, 2, 10, 16, 45, tzinfo=timezone.utc)
    end = datetime(2025, 2, 10, 16, 55, tzinfo=timezone.utc)

    # ✅ Convert to Unix timestamps
    start_time = int(start.timestamp())  
    end_time = int(end.timestamp())

    log_stream = "qa_aro-service"
    error_message = "QueryComposerFactory"

    print(f"🛠️ Testing CLI - Start Time (Unix): {start_time}, End Time (Unix): {end_time}")

    logs = get_logs_with_context(log_group, start_time, end_time, error_message, log_stream)

    # ✅ Print logs
    print("\n📌 Logs Around Error Occurrences:")
    for log in logs:
        print(log)
