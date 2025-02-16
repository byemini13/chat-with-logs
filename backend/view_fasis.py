import faiss
import numpy as np
import os

# Load FAISS index

import faiss

if not os.path.exists("java_embeddings.index"):
    print("⚠️ FAISS index missing! Rebuilding...")
    os.system("python recreate_java_embedings.py")
    
index = faiss.read_index("java_embeddings.index")
index = faiss.read_index("java_embeddings.index")

# Get details about the index
num_vectors = index.ntotal  # Total embeddings stored
vector_dimension = index.d  # Size of each vector

print(f"✅ FAISS index contains {num_vectors} embeddings, each of size {vector_dimension}.")
