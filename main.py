import json
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

with open("config.json") as f:
    config = json.load(f)

API_KEY = config["api_key"]
MODEL = config["model"]
INSTRUCTION = config.get("instruction", "")  # Get instruction from config
print(f"Using model: {MODEL} with instruction: {INSTRUCTION}")

app = FastAPI()

@app.get("/models")
def get_models():
    response = requests.get(
        "https://api.anthropic.com/v1/models",
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        }
    )
    resp_json = response.json()
    # Claude API returns models as a list under "data"
    models = [m["id"] for m in resp_json.get("data", [])]
    return JSONResponse(content={"models": models, "selected": MODEL})

@app.post("/set_model")
async def set_model(request: Request):
    data = await request.json()
    new_model = data.get("model")
    if new_model:
        config["model"] = new_model
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        global MODEL
        MODEL = new_model
        return JSONResponse(content={"success": True, "model": new_model})
    return JSONResponse(content={"success": False}, status_code=400)

@app.post("/prompt")
async def prompt(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "")
    # Prepend instruction if set
    full_prompt = f"{INSTRUCTION}\n{user_prompt}" if INSTRUCTION else user_prompt
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
            "messages": [{"role": "user", "content": full_prompt}]
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
          <label for="modelSelect">Model:</label>
          <select id="modelSelect" name="model"></select><br><br>
          <textarea name="prompt" rows="4" cols="50"></textarea><br>
          <button type="submit">Submit</button>
        </form>
        <br>
        <label for="result">Result:</label><br>
        <textarea id="result" rows="10" cols="80" readonly></textarea>
        <script>
          async function loadModels() {
            const res = await fetch('/models');
            const data = await res.json();
            const select = document.getElementById('modelSelect');
            select.innerHTML = '';
            data.models.forEach(model => {
              const opt = document.createElement('option');
              opt.value = model;
              opt.textContent = model;
              if (model === data.selected) opt.selected = true;
              select.appendChild(opt);
            });
          }
          document.getElementById('modelSelect').onchange = async function() {
            const model = this.value;
            await fetch('/set_model', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({model})
            });
          }
          document.getElementById('promptForm').onsubmit = async function(e) {
            e.preventDefault();
            const resultElem = document.getElementById('result');
            resultElem.value = "Processing...";
            const prompt = this.prompt.value;
            const res = await fetch('/prompt', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({prompt})
            });
            const data = await res.json();
            resultElem.value = data.content || "No response";
          }
          loadModels();
        </script>
      </body>
    </html>
    """