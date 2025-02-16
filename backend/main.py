from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from log_retrieval import get_logs_with_context
from code_retrieval import search_code
from llm_debugging import ask_gpt
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import List


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

class DebugRequest(BaseModel):
    logs: list
    code: list


@app.get("/logs")
def fetch_logs(log_group: str, log_stream: str, start_time: str, end_time: str, error_message: str = ""):
    start_timestamp = int(datetime.strptime(start_time, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc).timestamp())
    end_timestamp = int(datetime.strptime(end_time, "%Y-%m-%dT%H:%M").replace(tzinfo=timezone.utc).timestamp())

    logs = get_logs_with_context(log_group, start_timestamp, end_timestamp, error_message, log_stream)
    return {"logs": logs}

@app.post("/code")
def fetch_code(logs: list[str]):
    # Possibly convert the list of log lines into one big string 
    combined_text = "\n".join(logs)
    code = search_code(combined_text)
    return {"code": code}


@app.post("/debug")
def fetch_debug_info(request: DebugRequest):
    debug_info = ask_gpt(request.logs, request.code)
    return {"debug_info": debug_info}
