import json
import requests
import ollama
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="MCP Weather Web App")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

MCP_SERVER = "http://localhost:8000"

class WeatherRequest(BaseModel):
    city: str

class WeatherResponse(BaseModel):
    response: str
    city: str

POPULAR_CITIES = [
    "New York", "London", "Tokyo", "Paris", "Bhubaneswar", 
    "Bangalore", "San Francisco", "Sydney", "Dubai", "Berlin"
]

def get_mcp_tools():
    try:
        return requests.get(f"{MCP_SERVER}/tools").json()["tools"]
    except Exception:
        return []

def call_mcp_tool(name, payload):
    return requests.post(f"{MCP_SERVER}/tools/{name}", json=payload).json()

@app.get("/api/cities")
def get_cities():
    return {"cities": POPULAR_CITIES}

@app.post("/api/weather", response_model=WeatherResponse)
async def get_weather(request: WeatherRequest):
    user_query = f"What is the weather in {request.city}?"
    
    mcp_tools = get_mcp_tools()
    if not mcp_tools:
        raise HTTPException(status_code=503, detail="MCP Server is not reachable")

    ollama_tools = []
    for tool in mcp_tools:
        ollama_tools.append({
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool["description"],
                "parameters": tool["input_schema"]
            }
        })
        
    messages = [{"role": "user", "content": user_query}]
    
    # 1. Ask LLM if it needs a tool
    response = ollama.chat(
        model='gemma4:e4b',
        messages=messages,
        tools=ollama_tools
    )
    
    if response.get("message", {}).get("tool_calls"):
        tool_call = response["message"]["tool_calls"][0]
        function_name = tool_call["function"]["name"]
        arguments = tool_call["function"]["arguments"]
        
        # 2. Call the tool
        tool_result = call_mcp_tool(function_name, arguments)
        
        # 3. Get final response from LLM
        messages.append(response["message"])
        messages.append({
            "role": "tool",
            "content": json.dumps(tool_result),
            "name": function_name
        })
        
        final_response = ollama.chat(
            model='gemma4:e4b',
            messages=messages
        )
        return {
            "response": final_response["message"]["content"],
            "city": request.city
        }
    
    return {
        "response": response["message"]["content"],
        "city": request.city
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
