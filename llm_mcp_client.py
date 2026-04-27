import requests
import json
import ollama

MCP_SERVER = "http://localhost:8000"

def get_tools():
    try:
        return requests.get(f"{MCP_SERVER}/tools").json()["tools"]
    except Exception as e:
        print(f"Error connecting to MCP server: {e}")
        return []

def call_tool(name, payload):
    return requests.post(f"{MCP_SERVER}/tools/{name}", json=payload).json()

def agent(user_query):
    # Fetch tools from MCP server
    mcp_tools = get_tools()
    
    # Format tools for Ollama
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
        
    messages = [
        {"role": "user", "content": user_query}
    ]
    
    # Call Ollama with tools
    print("Thinking...")
    response = ollama.chat(
        model='gemma4:e4b',
        messages=messages,
        tools=ollama_tools
    )
    
    # Check if the model decided to call a tool
    if response.get("message", {}).get("tool_calls"):
        for tool_call in response["message"]["tool_calls"]:
            function_name = tool_call["function"]["name"]
            arguments = tool_call["function"]["arguments"]
            
            print(f"Calling tool: {function_name} with args: {arguments}")
            
            # Execute the tool
            tool_result = call_tool(function_name, arguments)
            
            print(f"Tool result: {tool_result}")
            
            # Add tool result to messages
            messages.append(response["message"])
            messages.append({
                "role": "tool",
                "content": json.dumps(tool_result),
                "name": function_name
            })
            
            # Call Ollama again to generate final response
            print("Generating final response...")
            final_response = ollama.chat(
                model='gemma4:e4b',
                messages=messages
            )
            return final_response["message"]["content"]
            
    # If no tool was called, just return the response
    return response["message"]["content"]

if __name__ == "__main__":
    while True:
        try:
            query = input("\nAsk: ")
            if query.lower() in ['quit', 'exit']:
                break
            print("\nResponse:")
            print(agent(query))
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
