import os

def read_java_files(directory):
    """Recursively finds all Java files in a directory and reads their content."""
    code_snippets = []
    
    for root, _, files in os.walk(directory):  # Walk through all subdirectories
        for file in files:
            if file.endswith(".java"):  # Filter only Java files
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        code_snippets.append(f.read())
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
    
    return code_snippets

# Example: Provide the path to your local GitHub repo
java_code = read_java_files("C:/Users/ben.yemini/OneDrive - Altman Solon/Documents/GitHub/aro-service")

print(f"Loaded {len(java_code)} Java files.")
