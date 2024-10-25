from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

# Mount the directory containing images to a specific URL path
app.mount("/images", StaticFiles(directory="images"), name="images")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)