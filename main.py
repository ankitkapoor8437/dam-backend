from fastapi import FastAPI, UploadFile, File
from services.ingest import process_upload
from services.search import perform_search
from services.library import list_all_images
from core.db import DB
from fastapi.staticfiles import StaticFiles
from core.config import IMAGES_DIR
from fastapi.middleware.cors import CORSMiddleware

# Initialize App
app = FastAPI(title="Open Source Image DAM")

# CORS Configuration
origins = [
    "http://localhost",
    "http://localhost:8501", # Streamlit
    "http://localhost:5173", # Vite React,
    "https://clip-dam.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for image serving
app.mount("/images", StaticFiles(directory=IMAGES_DIR), name="images")

@app.on_event("startup")
async def startup_event():
    DB.init_sqlite()

@app.post("/ingest")
async def ingest_endpoint(file: UploadFile = File(...)):
    return process_upload(file)

@app.get("/search")
async def search_endpoint(query: str, limit: int = 5):
    return perform_search(query, limit)

@app.get("/images")
async def list_images_endpoint():
    return list_all_images()

@app.get("/")
def home():
    return {"message": "DAM API is running. Go to /docs for Swagger UI."}
