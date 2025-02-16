# **AI-Powered Observability Tool**

## **Overview**
This application is an **AI-powered observability tool** designed to help developers **diagnose and troubleshoot** application issues. By analyzing logs and retrieving **relevant code snippets** from a user-specified GitHub repository, the app leverages **AWS CloudWatch, OpenAI embeddings, FAISS, and a web-based interface** to streamline debugging and issue resolution.

---

## **How It Works**

### **1. User-Defined Code Repository Embedding**
- Users specify a **GitHub repository** containing their application code.
- The application scans and extracts **all source code files**.
- The `embed_java_v2.py` script:
  - **Embeds the code** using OpenAI’s `text-embedding-ada-002` model.
  - **Stores embeddings** in a **FAISS index** for efficient similarity-based searches.
  - **Supports multiple programming languages**, making the tool **language agnostic**.

### **2. Log Retrieval**
- The app queries **AWS CloudWatch logs** using `boto3`.
- It searches for error occurrences within a **user-defined time range**.
- The system extracts logs **with contextual entries** (±5 log lines) for debugging reference.

### **3. Code Retrieval**
- The extracted error message is used to **query the FAISS index**.
- The app searches for the **most relevant code snippets** related to the error across **multiple programming languages**.
- It returns **highly relevant code sections** based on vector similarity.

### **4. AI Debugging**
- The app **sends logs and matching code snippets** to **GPT-4 Turbo** for analysis.
- The AI identifies **root causes**, suggests **debugging steps**, and provides **fix recommendations**.

### **5. Results Display**
- The web-based UI presents debugging insights in a structured format:
  - **Error Logs**
  - **Matching Code Snippets**
  - **GPT-4 Debugging Analysis & Suggested Fixes**
- Users can interact with debugging insights directly from the **front-end interface**.

---

## **Workflow**
1. **User Selects a GitHub Repository**
   - The app **clones the repo** and reads source code files.
   - The `embed_java_v2.py` script **embeds and indexes** the code.

2. **User Inputs an Error Message or Timestamp**
   - The app queries **AWS logs** and extracts the relevant **error messages**.

3. **Finds Matching Code**
   - The app **queries FAISS** to find relevant code snippets associated with the error.

4. **AI-Powered Debugging**
   - The app sends **logs + code** to **GPT-4 Turbo** for **analysis and troubleshooting**.

5. **User Receives Debugging Insights**
   - The web interface displays **log context, matching code, and AI-generated suggestions**.

---

## **Tech Stack**

### **Back End**
- **AWS CloudWatch** → Log retrieval
- **OpenAI API** → Code embedding & GPT-4 debugging
- **FAISS** → Vector search for relevant code snippets
- **Python** (`boto3`, `numpy`, `json`, `faiss`, `openai`) → Core logic

### **Front End**
- **React.js / Next.js** → Web-based UI for log input, repo selection, and debugging output
- **FastAPI / Flask** → API for handling embeddings, log queries, and GPT-4 responses
- **Docker & Kubernetes** (Optional) → Deployment and scaling

---

## **Key Enhancements**
✔ **User-Defined GitHub Repositories** – Users can specify which repository to analyze.  
✔ **Language Agnostic** – Supports **multiple programming languages** beyond Java.  
✔ **Web-Based Front End** – Enables **log queries, repo selection, and debugging insights**.  
✔ **Scalable Architecture** – Uses **FAISS for efficient search**, OpenAI for **smart debugging**, and AWS CloudWatch for **log retrieval**.  

---

## **Specific UI Components**

### **1. Repository Selection Page**
- **Dropdown/Input Field**: Users can enter or select a GitHub repository.
- **Clone & Index Status**: Shows real-time status of repository embedding.
- **Multi-language Support Indicator**: Highlights supported programming languages.

### **2. Log Query Interface**
- **Time Range Selector**: Users can filter logs based on time duration.
- **Search by Error Message**: Input field for searching logs based on specific errors.
- **Live Log Feed**: Real-time logs display with auto-refresh option.
- **Filter Options**: By severity (INFO, WARN, ERROR), service name, or keyword.

### **3. Code Snippet Viewer**
- **Highlighted Code Blocks**: Displays relevant code snippets with syntax highlighting.
- **Expandable Sections**: Users can view the full source file if needed.
- **Code Versioning**: Shows repository commit history related to retrieved code.

### **4. AI Debugging Panel**
- **GPT-4 Analysis Display**: Presents AI-generated explanations and fix suggestions.
- **Interactive Debugging Assistant**: Users can refine questions and get follow-up insights.
- **Severity Rating**: AI assigns a confidence score to debugging suggestions.

### **5. Debugging History & Insights Dashboard**
- **Saved Debugging Sessions**: Users can revisit past analyses.
- **Comparison Mode**: Allows viewing past vs. present debugging logs and fixes.
- **Export Reports**: Download AI-generated debugging reports in PDF or JSON format.

---

## **Next Steps**
1. **Implement the front-end UI** to allow users to:
   - Select a **GitHub repository**.
   - Input an **error message** or **timestamp**.
   - View debugging insights.

2. **Enhance language support** by ensuring embeddings work with **Python, JavaScript, Go, C#, etc.**.

3. **Optimize FAISS indexing** for real-time updates when new code is pushed.

---

## **Future Considerations**
- **Real-time log monitoring & alerting** for proactive debugging.
- **Integration with CI/CD pipelines** for automated issue detection.
- **User feedback loop** to refine AI debugging accuracy over time.

---






