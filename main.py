from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Coachy API")

# CORS 設定（允許你的 Streamlit 或其他前端）
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/students")
def list_students():
    # 之後會改成讀 DB / Google Sheets
    return [
        {"id": 1, "name": "Alice", "status": "Active"},
        {"id": 2, "name": "Bob", "status": "Inactive"},
    ]
