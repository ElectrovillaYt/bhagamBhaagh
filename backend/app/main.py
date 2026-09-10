from fastapi import FastAPI

from app.modules.auth.router import router as auth_router

app = FastAPI(
    title="BhagamBhaagh API",
    version="0.1.0"
)

# Including Routes
app.include_router(auth_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "BhagamBhaagh API"
    }
