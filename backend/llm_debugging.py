import openai
import os
import json

openai.api_key = os.getenv("OPENAI_API_KEY")


def format_java_code(java_snippets):
    """Format retrieved Java code for better readability."""
    if isinstance(java_snippets, list):  # Ensure it's a list of snippets
        formatted_code = "\n\n".join(snippet.replace("\\n", "\n").replace("\\", "\\\\") for snippet in java_snippets)
    else:
        formatted_code = java_snippets.replace("\\n", "\n").replace("\\", "\\\\")  # Escape backslashes
    
    # Wrap in markdown format for better rendering
    return f"```java\n{formatted_code}\n```"

def format_logs(logs):
    """Convert logs into structured JSON for better readability."""
    try:
        return json.dumps(logs, indent=2)
    except Exception as e:
        print(f"❌ Error formatting logs: {e}")
        return str(logs)  # Fallback to string

def ask_gpt(logs, relevant_code):
    """Send structured logs + formatted Java code to GPT-4 for debugging."""
    
    formatted_code = format_java_code(relevant_code)  
    structured_logs = format_logs(logs)  

    prompt = f"""
    You are an expert Java developer and troubleshooting engineer. Below are error logs and relevant Java code.

    📌 **Error Logs (structured JSON):**
    ```json
    {structured_logs}
    ```

    📌 **Relevant Java Code:**
    {formatted_code}

    **Debugging Task:**  
    - Analyze the logs and Java code.
    - Identify the most likely **root cause** of the issue.
    - Suggest **fixes** with specific Java code changes.

    Respond with a **detailed explanation** and **proposed solution**.
    """

    response = openai.chat.completions.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# If running as a standalone script
if __name__ == "__main__":
    test_logs = ("2025-02-10T16:46:09.236373208Z - WHERE st_area(CAST(ca.geom AS GEOGRAPHY), false) * :metersPerPixel >= :minPixelSize "
                "2025-02-10T16:46:09.236375231Z -  AND ca.libraryId = :libraryId "
                "2025-02-10T16:46:09.236377392Z -  AND ST_Intersects(ST_MakeEnvelope(:xMin, :yMin, :xMax, :yMax, 4326), ca.geom) "
                "2025-02-10T16:46:09.236378996Z - "
                "2025-02-10T16:46:09.236380756Z - ORDER BY st_area(CAST(ca.geom AS GEOGRAPHY), false) DESC  LIMIT 20000 "
                "2025-02-10T16:46:09.244943785Z - 16:46:09.244 [main] DEBUG c.a.aro.vt.gao.QueryComposerFactory -  SQL ===> "
                "2025-02-10T16:46:09.244964076Z - SELECT "
                "2025-02-10T16:46:09.244968936Z - ST_AsText(ST_Transform(f.geom, 3857)) AS _geom_transform,f.id AS id,f.length_meters AS edge_length,f.id AS gid,ft.name AS feature_type_name,f.edge_feature_type AS spatial_edge_type,f.edge_construction_type AS edge_construction_type, f.size_category AS size_category,f.object_id AS object_id,f.edge_feature_type AS spatial_edge_type "
                "2025-02-10T16:46:09.244971824Z - FROM aro.edge_entity f "
                "2025-02-10T16:46:09.244974158Z -  JOIN aro.edge_feature_type ft ON ft.id = f.edge_feature_type "
                "2025-02-10T16:46:09.244976229Z -")
    test_code = ("package com.altvil.aro.model.client.plan;import com.altvil.aro.model.ComparableModel;"
                 "import com.altvil.aro.model.aro_core.DataConfigurationEntity;import com.altvil.aro.model.plan.config.PlanConfigEntity;"
                 "import com.altvil.aro.persistence.SerializationUtils;import com.altvil.aro.service.dmt.TransactionRecalcState;import "
                 "com.altvil.aro.core.service.price.engine.ComputedState;import com.altvil.enumerations.PlanTransactionState;import com.altvil.interfaces.type.DataType;"
                 "import com.vladmihalcea.hibernate.type.array.StringArrayType;import org.hibernate.annotations.Type;import jakarta.persistence.*;import java.io.Serializable;"
                 "import java.util.Arrays;import java.util.Date;import java.util.Set;import java.util.stream.Collectors;import static jakarta.persistence.GenerationType.IDENTITY;"
                 "@Entity@Table(name = plan_transaction, schema = client)public class PlanTransactionEntity extends ComparableModel {private Long id;private Date startDate"
                 " = new Date();private Date initializationStartDate = new Date();private Date initializationEndDate;private Date commitDate;private Integer userId;private"
                 "PlanTransactionState state;private Long planId;private SubnetRecalcType subnetRecalcType;private PlanTransactionType planTransactionType;tprivate int workspaceId")

    response = ask_gpt(test_logs, test_code)
    print("\n🚀 GPT-4 Debugging Response:", response)
