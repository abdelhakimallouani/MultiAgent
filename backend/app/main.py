from fastapi import FastAPI
from app.api.auth import router as auth_router

from app.api.agent import router as agent_router

app = FastAPI()

app.include_router(
    auth_router,
    prefix="/api/auth",
    tags=["Auth"]
)

app.include_router(
    agent_router,
    prefix="/api/agents",
    tags=["Agents"]
)