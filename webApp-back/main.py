import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.middleware import login_required_middleware
from dotenv import load_dotenv

# Import routers from the api folder
from api import monitoring, camera, signin

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Add Global Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.middleware("http")(login_required_middleware)

# Include all routers
app.include_router(monitoring.router, tags=["Monitoring"])
app.include_router(camera.router, tags=["Camera & WebSocket"])
app.include_router(signin.router, tags=["Sign In"])

@app.get("/")
def root():
    return {"message": "Face Detection API is running"}

# Main execution point
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=3001, reload=True)