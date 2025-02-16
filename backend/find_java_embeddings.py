import os
import faiss

if not os.path.exists("java_embeddings.index"):
    print("⚠️ FAISS index missing! Rebuilding...")
    os.system("python recreate_java_embedings.py")
    
index = faiss.read_index("java_embeddings.index")

file_path = "java_embeddings.json"
print("Exists:", os.path.exists(file_path))
print("Absolute Path:", os.path.abspath(file_path))
