# SkyMCP: Premium Web Weather App using MCP & Ollama

SkyMCP is a highly interactive, premium weather dashboard that leverages the **Model Context Protocol (MCP)** and a local **Ollama** model (`gemma4:e4b`) to provide conversational weather reports.

## Features
- **Premium UI**: Glassmorphism design with Framer Motion animations.
- **MCP Integration**: Uses a standardized protocol to fetch real-time weather data.
- **Local LLM**: Powered by Google's Gemma 4 (via Ollama) for intelligent data synthesis.
- **FastAPI Backend**: A high-performance bridge between the AI and the web frontend.

## Architecture
For a detailed technical breakdown, see [architecture.md](./architecture.md).

## Prerequisites
- **[uv](https://docs.astral.sh/uv/)**: Fast Python package manager.
- **[Node.js & npm](https://nodejs.org/)**: For the React frontend.
- **[Ollama](https://ollama.com/)**: To run the local LLM (`ollama pull gemma4:e4b`).
- **OpenWeather API Key**: [Get one here](https://openweathermap.org/api).

## Installation

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/hellonihar/web_utility_to_check_weather_MCP_Local_LLM.git
   cd web_utility_to_check_weather_MCP_Local_LLM
   ```

2. **Configure Environment**:
   Create a `.env` file in the root:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

3. **Backend Setup**:
   ```bash
   uv venv
   # Windows: .venv\Scripts\activate | Unix: source .venv/bin/activate
   uv pip install mcp fastapi uvicorn ollama httpx pydantic requests python-dotenv
   ```

4. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   ```

## Operating Instructions

To run the full application, you will need **three terminal windows**:

### 1. Start the MCP Weather Server
This provides the raw weather tools:
```bash
uvicorn mcp_weather_server:app --port 8000
```

### 2. Start the Web Backend
This orchestrates the LLM and MCP logic:
```bash
python main.py
```
*(Running on http://localhost:8001)*

### 3. Start the Frontend
The user interface:
```bash
cd frontend
npm run dev
```
*(Running on http://localhost:5173)*

## How to Use
1. Open [http://localhost:5173](http://localhost:5173) in your browser.
2. Select a city from the premium dropdown.
3. Click **"Show Weather"**.
4. Watch as the AI fetches real-time data via MCP and generates a natural language report.
