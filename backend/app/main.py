"""
FastAPI Application Factory
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from app.core.event_bus import event_bus
from app.api.health import router as health_router
from app.api.v1.routes import chat, voice, memory, agents, tasks, models, files, system
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    """
    logger.info("HUGO Starting...")
    await event_bus.initialize()
    yield
    logger.info("HUGO Shutting down...")
    await event_bus.shutdown()


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    app = FastAPI(
        title="HUGO AI Operating System",
        description="Self-hosted JARVIS-style AI assistant",
        version="1.0.0",
        lifespan=lifespan
    )
    
    # CORS Configuration
    cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "type": type(exc).__name__}
        )
    
    # Include routers
    app.include_router(health_router, tags=["health"])
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
    app.include_router(voice.router, prefix="/api/v1/voice", tags=["voice"])
    app.include_router(memory.router, prefix="/api/v1/memory", tags=["memory"])
    app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
    app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])
    app.include_router(models.router, prefix="/api/v1/models", tags=["models"])
    app.include_router(files.router, prefix="/api/v1/files", tags=["files"])
    app.include_router(system.router, prefix="/api/v1/system", tags=["system"])
    
    return app


app = create_app()
