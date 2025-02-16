import faiss
import numpy as np
import json
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

# Load FAISS index
if not os.path.exists("java_embeddings.index"):
    print("⚠️ FAISS index missing! Rebuilding...")
    os.system("python recreate_java_embedings.py")
    
index = faiss.read_index("java_embeddings.index")
index = faiss.read_index("java_embeddings.index")

# Load Java snippets
with open("java_embeddings.json", "r", encoding="utf-8") as f:
    java_data = json.load(f)

java_code = [item["code"] for item in java_data]

def search_code(error_message, k=3):
    """Finds relevant Java snippets for a given error message."""
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=error_message
    )
    query_embedding = np.array(response.data[0].embedding).reshape(1, -1)

    _, indices = index.search(query_embedding, k)
    
    return [java_code[i] for i in indices[0]]

# If running as a standalone script
if __name__ == "__main__":
    query = ("2025-02-10T16:46:09.236373208Z - WHERE st_area(CAST(ca.geom AS GEOGRAPHY), false) * :metersPerPixel >= :minPixelSize "
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
    relevant_snippets = search_code(query)
    print("\n📌 Relevant Java Snippets:", relevant_snippets)
