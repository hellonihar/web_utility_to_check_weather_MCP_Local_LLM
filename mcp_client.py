import requests
import json

MCP_SERVER = "http://localhost:8000"

def get_tools():
    return requests.get(f"{MCP_SERVER}/tools").json()["tools"]

def call_tool(name, payload):
    return requests.post(f"{MCP_SERVER}/tools/{name}", json=payload).json()


def agent(user_query):
    tools = get_tools()

    # VERY SIMPLE ROUTER (replace with LLM later)
    if "weather" in user_query.lower():
        # naive city extraction
        words = user_query.split()
        city = words[-1]

        result = call_tool("get_weather", {"city": city})

        if "error" in result:
            return f"Error: {result['error']}"

        return (
            f"Weather in {result['city']}:\n"
            f"Temp: {result['temperature']}°C\n"
            f"Humidity: {result['humidity']}%\n"
            f"Condition: {result['description']}\n"
            f"Wind Speed: {result['wind_speed']} m/s"
        )

    return "I can help with weather queries."


if __name__ == "__main__":
    while True:
        query = input("Ask: ")
        print(agent(query))