import boto3
import time
import json
from datetime import datetime, timedelta, timezone

client = boto3.client("logs")

def get_logs_with_context(log_group, start_timestamp, end_timestamp, error_message, log_stream, limit=5, max_occurrences=3):
    """Fetch logs from AWS CloudWatch, including 5 logs before & after each error occurrence."""
    
    # 1️⃣ Step 1: Retrieve ALL logs in the time range
    query_all = f'''
        fields @timestamp, @message
        | filter @logStream like "{log_stream}"
        | sort @timestamp asc
    '''
    
    try:
        response = client.start_query(
            logGroupName=log_group,
            startTime=int(start_time.timestamp()),
            endTime=int(end_time.timestamp()),
            queryString=query_all,
        )
    except Exception as e:
        print(f"❌ AWS CloudWatch Query Failed: {e}")
        return []

    query_id = response["queryId"]
    
    # Wait for query results
    while True:
        result = client.get_query_results(queryId=query_id)
        if result["status"] in ["Complete", "Failed", "Cancelled"]:
            break
        time.sleep(2)
    
    # 2️⃣ Step 2: Parse logs & extract relevant messages
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

    # 3️⃣ Step 3: Find all occurrences of the error
    error_indices = [i for i, log in enumerate(all_logs) if error_message in log["log"]]

    if not error_indices:
        print("❌ No logs found matching the error message.")
        return []

    print(f"🔍 Found {len(error_indices)} occurrences of the error message.")

    # 4️⃣ Step 4: Retrieve logs within ±5 range of each error (limit occurrences if needed)
    logs_with_context = []
    for index, error_index in enumerate(error_indices[:max_occurrences]):  # Limit occurrences
        start_index = max(0, error_index - 5)
        end_index = min(len(all_logs), error_index + 6)  # +6 to include the error itself

        context_logs = all_logs[start_index:end_index]
        formatted_logs = [f"{log['timestamp']} - {log['log']}" for log in context_logs]

        logs_with_context.append(f"\n🛑 **Context around Error Occurrence {index + 1}**:")
        logs_with_context.extend(formatted_logs)

    return logs_with_context


# Example usage
log_group = "/aws/containerinsights/nonprod/application"

#absolute time
# 🔹 Set a precise start & end time (e.g., Feb 10, 2025, 16:45 to 16:55 UTC)
start_time = datetime(2025, 2, 10, 16, 45, tzinfo=timezone.utc)  # 16:45:00 UTC
end_time = datetime(2025, 2, 10, 16, 55, tzinfo=timezone.utc)  # 16:55:00 UTC
start_timestamp = int(start_time.timestamp())  # Convert to Unix time
end_timestamp = int(end_time.timestamp())

#relative time 
#start_timestamp = datetime.now(timezone.utc) - timedelta(hours=12)  # Last 1 hour
#end_timestamp = datetime.now(timezone.utc)
error_message = "QueryComposerFactory "
log_stream = "qa_aro-service"  # Specify the exact log stream name

logs = get_logs_with_context(log_group, start_time, end_time, error_message, log_stream)

# Print cleaned logs
print("\n📌 Logs Around Error Occurrences:")
for log in logs:
    print(log)