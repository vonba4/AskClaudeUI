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
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        },
        json={
            "model": MODEL,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": user_prompt}]
        }
    )
    # Extract the content text field from the response
    resp_json = response.json()
    content_text = ""
    if "content" in resp_json and isinstance(resp_json["content"], list):
        # Claude API returns a list of content blocks
        content_text = "".join([block.get("text", "") for block in resp_json["content"]])
    return JSONResponse(content={"content": content_text})

@app.get("/", response_class=HTMLResponse)
def index():
    return """
    <html>
      <body>
        <h1>Ask Claude UI</h1>
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
            document.getElementById('result').textContent = data.content || "No response";
          }
        </script>
      </body>
    </html>
    """