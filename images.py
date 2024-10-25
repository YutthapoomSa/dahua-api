from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import importlib

app = FastAPI()

# Mount the directory containing images to a specific URL path
# app.mount("/images", StaticFiles(directory="images"), name="images")

@app.on_event("startup")
async def startup_event():
    # Dynamically import and call the callback function from main22.py
    local_function = importlib.import_module("main22")
    result = local_function.start_listen_events()
    print(result)

@app.get("/")
async def root():
    return {"message": "hello from python"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)