
"use client";

import React, { useState, useEffect } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { Table } from "@/components/ui/table";

export default function DebuggingUI() {
  const [startTime, setStartTime] = useState<string>("");
  const [endTime, setEndTime] = useState<string>("");
  const [hydrated, setHydrated] = useState(false);  
  const [logs, setLogs] = useState<string[]>([]); // ✅ Ensure logs is always an array of strings
  const [codeSnippets, setCodeSnippets] = useState<[string, string][]>([]);
  const [debugInfo, setDebugInfo] = useState<string>("");
  const [logGroup, setLogGroup] = useState("");
  const [logStream, setLogStream] = useState("");
  const [errorMessageInput, setErrorMessageInput] = useState(""); // User input
  const [logErrorMessage, setLogErrorMessage] = useState(""); // API errors

  const [errorMessage, setErrorMessage] = useState("");
  const [hasQueried, setHasQueried] = useState(false); // ✅ Track if a log query was made
  const [analysis, setAnalysis] = useState("");
  const [activeTab, setActiveTab] = useState("logs");

 
  // ✅ Set the time after hydration to avoid mismatch
  useEffect(() => {
    if (typeof window !== "undefined") {
      setHydrated(true);
      const now = new Date().toISOString().slice(0, 16);
      setStartTime(now);
      setEndTime(now);
    }
  }, []);

  
  const logStreamOptions: Record<string, string[]> = {
      "production": ["Windstream", "Consolidated", "JSI","123net" ],
      "non-production": ["QA", "UAT"]
  };

  const resolveLogGroup = (group: string) => {
    const logGroupMap: Record<string, string> = {
        "production": "/aws/containerinsights/prod/application",
        "non-production": "/aws/containerinsights/nonprod/application"
    };

    return logGroupMap[group] || ""; // ✅ Return an empty string if invalid
};


  const resolveLogStream = (stream: string) => {
    const logStreamMap: Record<string, string> = {
        "QA": "qa_aro-service",
        "UAT": "uat_aro-service",
        "Windstream": "windstream-aro-service",
        "Consolidated": "consolidated-aro-service",
        "JSI": "jsi-aro-service",
        "123net": "123net-aro-service"
    };

    return logStreamMap[stream] || stream; // ✅ Default to the same value if not found
};

const handleLogGroupChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
  const selectedGroup = e.target.value;
  setLogGroup(selectedGroup);
  setLogStream(""); // ✅ Reset log stream selection when log group changes
};

const handleLogStreamChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
  setLogStream(e.target.value);
};

const fetchLogs = async () => {
  if (!hydrated || !startTime || !endTime) {
    console.warn("⏳ Waiting for hydration... Start time or end time is not set yet.");
    return;
  }

  if (!logGroup || !logStream || !errorMessageInput) {
    console.warn("⚠️ Missing required input fields!");
    return;
  }

  setHasQueried(true);

  // ✅ Format API parameters
  const formattedLogGroup = encodeURIComponent(resolveLogGroup(logGroup));
  const formattedLogStream = encodeURIComponent(resolveLogStream(logStream));
  const encodedStartTime = encodeURIComponent(startTime);
  const encodedEndTime = encodeURIComponent(endTime);
  const encodedErrorMessage = encodeURIComponent(errorMessageInput);

  const apiUrl = `http://127.0.0.1:8000/logs?log_group=${formattedLogGroup}&log_stream=${formattedLogStream}&start_time=${encodedStartTime}&end_time=${encodedEndTime}&error_message=${encodedErrorMessage}`;

  console.log("🚀 Fetching logs from:", apiUrl);

  try {
    const response = await fetch(apiUrl);
    const data = await response.json();

    console.log("🔍 API Response:", data);

    // ✅ Handle API errors
    if (data.error) {
      setLogErrorMessage(data.error);
      setLogs([]);
      setCodeSnippets([]); // ✅ Clear previous code snippets
      setAnalysis(""); // ✅ Clear previous AI analysis
      return;
    }

    // ✅ Store logs (ensure it's an array)
    setLogs(Array.isArray(data.logs) ? data.logs : []);
    setLogErrorMessage("");

    // ✅ Store Relevant Code Snippets
    if (Array.isArray(data.codeSnippets) && data.codeSnippets.length > 0) {
      setCodeSnippets([...data.codeSnippets]); // ✅ Force state update
      setActiveTab("code"); // ✅ Auto-switch to Code tab
    } else {
      setCodeSnippets([]);
    }

    // ✅ Store AI Debugging Analysis
    if (typeof data.analysis === "string" && data.analysis.trim() !== "") {
      setAnalysis(data.analysis);
      setActiveTab("analysis"); // ✅ Auto-switch to Analysis tab
    } else {
      setAnalysis("");
    }
  } catch (error) {
    console.error("❌ Error fetching logs:", error);
    setLogs([]);
    setCodeSnippets([]);
    setAnalysis("");
    setLogErrorMessage("Error fetching logs. Please try again.");
  }
};

const fetchCode = async () => {
  if (logs.length === 0) {
    console.warn("⚠️ No logs available. Fetch logs first.");
    return;
  }

  const apiUrl = "http://127.0.0.1:8000/code";  
  
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ logs }), 
      });

    const data = await response.json();

    console.log("🔍 API Response for Code:", data);

    if (data.error) {
      setCodeSnippets([]);
    } else {
      // Suppose your server returns { code: ["snippet1", "snippet2", ...] }
      // So data.code is an array. Convert it to the shape you want:
      setCodeSnippets([...data.code]);
      setActiveTab("code"); // ✅ Auto-switch to Code tab
    }
  } catch (error) {
    console.error("❌ Error fetching code:", error);
    setCodeSnippets([]);
  }
};

const fetchDebugInfo = async () => {
  if (logs.length === 0 || codeSnippets.length === 0) {
    console.warn("⚠️ Fetch logs and code first.");
    return;
  }

  const apiUrl = `http://127.0.0.1:8000/debug`;

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ logs, code: codeSnippets })
    });

    const data = await response.json();

    console.log("🔍 API Response for Debugging:", data);

    if (data.error) {
      setDebugInfo("");
    } else {
      setDebugInfo(data.debug_info);
      setAnalysis(data.debug_info);
      setActiveTab("analysis"); // ✅ Auto-switch to Analysis tab
    }
  } catch (error) {
    console.error("❌ Error fetching debugging info:", error);
    setDebugInfo("");
  }
};


const isGetLogsEnabled = logGroup && logStream && startTime && endTime && errorMessageInput;
const isGetCodeEnabled = logs.length > 0;
const isDebugEnabled = logs.length > 0 && codeSnippets.length > 0;

return (
  <div className="p-6 space-y-6">
    <Card>
      <h2 className="text-xl font-semibold">Log Retrieval</h2>
      <div className="space-y-4 flex flex-col">

        {/* Log Group Dropdown */}
        <label>Log Group:</label>
        <select 
          value={logGroup} 
          onChange={handleLogGroupChange}
          className="border p-2 rounded-md"
        >
          <option value="">Select Log Group</option>
          <option value="production">Production</option>
          <option value="non-production">Non-Production</option>
        </select>

        {/* Log Stream Dropdown */}
        <label>Log Stream:</label>
        <select 
          value={logStream} 
          onChange={handleLogStreamChange}
          className="border p-2 rounded-md"
          disabled={!logGroup}
        >
          <option value="">Select Log Stream</option>
          {logGroup &&
            logStreamOptions[logGroup]?.map((stream) => (
              <option key={stream} value={stream}>{stream}</option>
            ))
          }
        </select>

        <label>Start Time:</label>
        <Input type="datetime-local" value={startTime} onChange={(e) => setStartTime(e.target.value)} />

        <label>End Time:</label>
        <Input type="datetime-local" value={endTime} onChange={(e) => setEndTime(e.target.value)} />

        <label>Error Message:</label>
        <Input type="text" value={errorMessageInput} onChange={(e) => setErrorMessageInput(e.target.value)} />
        <div className="flex space-x-4">
          <Button onClick={fetchLogs} disabled={!isGetLogsEnabled}>Get Logs</Button>
          <Button onClick={fetchCode} disabled={!isGetCodeEnabled}>Get Code</Button>
          <Button onClick={fetchDebugInfo} disabled={!isDebugEnabled}>Debug</Button>
        </div>
      </div>
    </Card>
    <Tabs defaultValue="logs">
      <TabsList>
      <TabsTrigger value="logs">Logs</TabsTrigger>
      <TabsTrigger value="code">Code</TabsTrigger>
      <TabsTrigger value="analysis">Analysis</TabsTrigger>
    </TabsList>

    <TabsContent value="logs">
      {logs.map((line, i) => <div key={i}>{line}</div>)}
    </TabsContent>

    <TabsContent  value="code">
      {codeSnippets.map((snippet, i) => (
        <pre key={i}>{snippet}</pre>
      ))}
    </TabsContent>

    <TabsContent value="analysis">
      <pre>{analysis}</pre>
    </TabsContent>
  </Tabs>
  </div>
);
}