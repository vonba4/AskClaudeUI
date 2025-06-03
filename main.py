import json
import os
import requests
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

# Use a config folder for config.json
CONFIG_PATH = os.path.join("cfg", "config.json")
with open(CONFIG_PATH) as f:
    config = json.load(f)

API_KEY = config["api_key"]
MODEL = config["model"]
INSTRUCTION = config.get("instruction", "")
TEMPERATURE = config.get("temperature", 1.0)

print(f"Using model: {MODEL} with instruction: {INSTRUCTION}")

app = FastAPI()

# Mount the frontend static files (HTML, JS, CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        global MODEL
        MODEL = new_model
        return JSONResponse(content={"success": True, "model": new_model})
    return JSONResponse(content={"success": False}, status_code=400)

@app.post("/set_instruction")
async def set_instruction(request: Request):
    data = await request.json()
    new_instruction = data.get("instruction")
    if new_instruction is not None:
        config["instruction"] = new_instruction
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        global INSTRUCTION
        INSTRUCTION = new_instruction
        return JSONResponse(content={"success": True, "instruction": new_instruction})
    return JSONResponse(content={"success": False}, status_code=400)

@app.post("/set_temperature")
async def set_temperature(request: Request):
    data = await request.json()
    new_temperature = data.get("temperature")
    if new_temperature is not None:
        config["temperature"] = new_temperature
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        global TEMPERATURE
        TEMPERATURE = new_temperature
        return JSONResponse(content={"success": True, "temperature": new_temperature})
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
            "temperature": TEMPERATURE,
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
    # Serve the frontend HTML from the static folder
    with open(os.path.join("static", "index.html")) as f:
        return HTMLResponse(f.read())

@app.get("/config")
def get_config():
    # Expose only safe config values
    return JSONResponse(content={
        "instruction": config.get("instruction", ""),
        "temperature": config.get("temperature", 1.0)
    })