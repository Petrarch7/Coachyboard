from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Coachy API")

# CORS 設定
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 首頁
@app.get("/")
def root():
    return {"message": "Welcome to Coachy API 🎉", "docs": "/docs"}

# 健康檢查
@app.get("/health")
def health():
    return {"status": "ok"}

# 學生清單
@app.get("/students")
def list_students():
    return [
        {"id": 1, "name": "Alice", "status": "Active"},
        {"id": 2, "name": "Bob", "status": "Inactive"},
    ]
