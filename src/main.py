from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
import json
from pathlib import Path

app= FastAPI()
API_KEY = None
file_path = Path(__file__).parent.parent / 'config.json'  # Equivalent to ../config.json

# Open and load the JSON file
with open(file_path, 'r') as f:
    print(f)
    data = json.load(f) 
    API_KEY = data.get("API_KEY")



@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if not (("/doc" in str(request.url) )or ("/openapi.json" in str(request.url))):
        api_key = request.headers.get("X-API-KEY", False)
        if not api_key:
            return JSONResponse(content={"message":"API_KEY not found"}, status_code=401)
        if api_key != API_KEY:
            return JSONResponse(content={"message":"Invalid API_KEY"}, status_code=401)
    response = await call_next(request)
    return response


@app.get("/hello")
def home():
    return JSONResponse(content={"message": "Welcome to Video verse task"})