import openai
import os
import time
import tiktoken  # Helps count tokens
import faiss
import numpy as np 
import json
import backoff 

# 1️⃣ Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 2️⃣ Read Java Files
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
                    print(f"Error reading {file_path}: {e}")
    return code_snippets

java_code = read_java_files("C:/Users/ben.yemini/OneDrive - Altman Solon/Documents/GitHub/aro-service")
print(f"✅ Loaded {len(java_code)} Java files.")  # ✅ Debugging

# 3️⃣ Token Counter Function
def count_tokens(text, model="text-embedding-ada-002"):
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# 4️⃣ Corrected Chunking Function
def chunk_text(text, max_tokens=7000):  # Reduce to 7000 for safety
    """Splits text into chunks ensuring they stay within the token limit."""
    encoding = tiktoken.encoding_for_model("text-embedding-ada-002")
    tokens = encoding.encode(text)  # Convert text into tokens
    
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = tokens[i:i + max_tokens]  # Extract a chunk
        chunks.append(encoding.decode(chunk))  # Convert back to text
    
    return chunks

# 5️⃣ Embedding Functions
# handle api rate limits 
@backoff.on_exception(backoff.expo, openai.error.RateLimitError, max_time=30)
def get_embedding(text):
    """Fetch embedding from OpenAI API with exponential backoff."""
    response = openai.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def embed_code(snippets):
    embeddings = []
    
    for snippet in snippets:
        # 🔹 Split large files into smaller chunks
        chunks = chunk_text(snippet)
        for chunk in chunks:
            chunk_tokens = count_tokens(chunk)  # Get token count
            print(f"🔹 Sending {chunk_tokens} tokens to OpenAI...")  # Debugging

            if chunk_tokens > 8192:
                print(f"❌ WARNING: Chunk exceeds 8192 tokens! It has {chunk_tokens} tokens.")

            try:
                embedding = get_embedding(chunk)  # Calls the retried function
                embeddings.append(embedding)
            except Exception as e:
                print(f"❌ Error embedding chunk: {e}")
        
    return embeddings

# 6️⃣ Run Embedding Process
java_embeddings = embed_code(java_code)
print(f"✅ Generated {len(java_embeddings)} embeddings.")

# 7️⃣ Save Embeddings & Code Snippets to JSON
def save_embeddings_json(filename, embeddings, code_snippets):
    """Save embeddings and code snippets to a JSON file."""
    data = [{"embedding": emb.tolist(), "code": snippet} for emb, snippet in zip(embeddings, code_snippets)]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# Save Java embeddings and code
save_embeddings_json("java_embeddings.json", java_embeddings, java_code)
print("✅ Saved embeddings & Java code to `java_embeddings.json`.")

# Convert embeddings to NumPy array
embedding_dim = len(java_embeddings[0])  # Get embedding size
index = faiss.IndexFlatL2(embedding_dim)
index.add(np.array(java_embeddings))  # Add embeddings

# Save FAISS index
faiss.write_index(index, "java_embeddings.index")

