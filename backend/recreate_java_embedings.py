import json
import os

# Check if FAISS index exists
if not os.path.exists("java_embeddings.index"):
    raise FileNotFoundError("❌ `java_embeddings.index` not found! Run the embedding script again.")

# If Java source code directory is available, rebuild JSON
java_source_dir = "C:/Users/ben.yemini/OneDrive - Altman Solon/Documents/GitHub/aro-service"  # Update with correct path

def read_java_files(directory):
    """Recursively reads all Java files in a directory."""
    code_snippets = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code_snippets.append(f.read())
                except Exception as e:
                    print(f"⚠️ Error reading {file_path}: {e}")
    return code_snippets

# Read Java files
java_code = read_java_files(java_source_dir)

# Ensure the number of code snippets matches FAISS embeddings
if len(java_code) == 0:
    raise ValueError("❌ No Java files found in the specified directory!")

# Save reconstructed JSON
json_data = [{"code": snippet} for snippet in java_code]
with open("java_embeddings.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4)

print("✅ `java_embeddings.json` successfully reconstructed!")
