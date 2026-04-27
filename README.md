# Basic Weather Check CLI using MCP

A natural language weather query tool powered by the **Model Context Protocol (MCP)** and a local **Ollama** model (`gemma4:e4b`). This application demonstrates how to bridge local LLMs with external APIs using standardized tool-calling protocols.

## Architecture

The system follows a modular architecture:
- **MCP Weather Server**: A FastAPI-based server that acts as an MCP provider, exposing a `get_weather` tool.
- **LLM MCP Client**: An intelligent agent that dynamically discovers tools from the server and uses a local LLM to orchestrate tool calls and summarize results.

For a detailed technical breakdown and Mermaid diagram, refer to [architecture.md](./architecture.md).

## Prerequisites

- **[uv](https://docs.astral.sh/uv/)**: A fast Python package and environment manager.
- **[Ollama](https://ollama.com/)**: Required to run the local LLM.
- **`gemma4:e4b` Model**: Pull the model using `ollama pull gemma4:e4b`.
- **OpenWeather API Key**: Get a free key from [OpenWeatherMap](https://openweathermap.org/api).

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hellonihar/basic_weather_check_CLI_using_MCP.git
   cd basic_weather_check_CLI_using_MCP
   ```

2. **Setup environment variables**:
   Create a `.env` file in the root directory and add your OpenWeather API key:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

3. **Initialize the environment**:
   ```bash
   uv venv
   # Windows: .venv\Scripts\activate
   # Unix: source .venv/bin/activate
   uv pip install mcp fastapi uvicorn ollama httpx pydantic requests python-dotenv
   ```

## Usage

1. **Start the MCP Weather Server**:
   In your first terminal, launch the server that provides the weather tools:
   ```bash
   uvicorn mcp_weather_server:app --port 8000
   ```

2. **Run the LLM MCP Client**:
   In a second terminal, run the interactive client:
   ```bash
   uv run llm_mcp_client.py
   ```

3. **Interact with the Agent**:
   Once the client is running, you can ask for weather in plain English:
   - `Ask: What is the weather like in Bhubaneswar?`
   - `Ask: Should I carry an umbrella in London today?`

## Project Structure

- `mcp_weather_server.py`: The FastAPI server implementing the weather tool.
- `llm_mcp_client.py`: The agentic client using Ollama for natural language processing.
- `architecture.md`: Detailed architectural documentation.
- `mcp_client.py`: A simple, non-LLM reference client.
