import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

with open("config.json") as f:
    config = json.load(f)

API_KEY = config["api_key"]
MODEL = config["model"]

app = FastAPI()

@app.post("/prompt")
async def prompt(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "")
    # Replace with the actual Claude Code API endpoint and payload structure
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": API_KEY,
            "content-type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": user_prompt}]
        }
    )
    return JSONResponse(content=response.json())

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
      <body>
        <h1>Claude Code UI</h1>
        <form id="promptForm">
          <textarea name="prompt" rows="4" cols="50"></textarea><br>
          <button type="submit">Submit</button>
        </form>
        <pre id="result"></pre>
        <script>
          document.getElementById('promptForm').onsubmit = async function(e) {
            e.preventDefault();
            const prompt = this.prompt.value;
            const res = await fetch('/prompt', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({prompt})
            });
            const data = await res.json();
            document.getElementById('result').textContent = JSON.stringify(data, null, 2);
          }
        </script>
      </body>
    </html>
    """