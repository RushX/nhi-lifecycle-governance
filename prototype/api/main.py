from fastapi import FastAPI
from database import engine, Base
from routers import agents

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Agent Identity Registry",
    description="Lifecycle governance for AI agent identities",
    version="0.1.0"
)

app.include_router(agents.router)

@app.get("/")
def root():
    return {
        "service": "AI Agent Identity Registry",
        "version": "0.1.0",
        "status": "running"
    }