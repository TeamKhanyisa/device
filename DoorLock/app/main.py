from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.register_api import router as register_router
from app.api.compare_api import router as compare_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://172.111.121.77:3000",
        "http://172.111.121.77:3000",
        "http://localhost:3000",
        "https://localhost:3000",
    ],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(register_router)
app.include_router(compare_router)
