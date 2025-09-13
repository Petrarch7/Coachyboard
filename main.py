from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
import os

app = FastAPI(title="Coachy API")

# ===== CORS =====
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Simple Token Auth =====
API_TOKEN = os.getenv("API_TOKEN", "")

def require_token(x_api_token: str = Header(None)):
    if not API_TOKEN:
        raise HTTPException(status_code=500, detail="API_TOKEN not configured")
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

# ===== Routes =====
@app.get("/")
def root():
    return {"message": "Welcome to Coachy API 🎉", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/students")
def list_students():
    return [
        {"id": 1, "name": "Alice", "status": "Active"},
        {"id": 2, "name": "Bob", "status": "Inactive"},
    ]

# ✅ 受保護路由：需要 X-API-Token
@app.get("/secret", dependencies=[Depends(require_token)])
def secret():
    return {"message": "這是保護內容 ✅ 只有帶正確 X-API-Token 才能看到"}

# ===== OpenAPI: 讓 /docs 顯示 Token 欄位 =====
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(title=app.title, version="1.0.0", routes=app.routes)
    openapi_schema.setdefault("components", {}).setdefault("securitySchemes", {})["ApiTokenHeader"] = {
        "type": "apiKey", "in": "header", "name": "X-API-Token"
    }
    for path in openapi_schema.get("paths", {}).values():
        for m in path.values():
            m.setdefault("security", [{"ApiTokenHeader": []}])
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
