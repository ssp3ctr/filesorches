from fastapi import FastAPI
from app.api.v1 import storage

app = FastAPI(title="Storage Orchestrator")

app.include_router(storage.router, prefix="/api/v1", tags=["Files"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
