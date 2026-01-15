"""
FastAPI application entry point.

Configures the API server, middleware, and route handlers.
"""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import get_settings
from app.core.exceptions import ChatbotException
from app.api.routes import health, chat

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.

    Initializes services on startup and closes connections on shutdown.
    """
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")

    # Initialize services
    from app.db.qdrant import get_qdrant_service
    from app.db.neon import get_neon_service

    # Initialize Qdrant (required)
    qdrant = get_qdrant_service()
    try:
        await qdrant.initialize_collection()
        logger.info("Qdrant service initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Qdrant: {e}")
        raise

    # Initialize Neon (optional - analytics)
    neon = get_neon_service()
    neon.initialize_pool()  # Won't raise if it fails
    if neon.is_initialized():
        logger.info("Neon analytics service initialized")
    else:
        logger.info("Neon analytics service not available")

    yield

    # Cleanup on shutdown
    logger.info("Shutting down services...")
    await qdrant.close()
    await neon.close()
    logger.info("Services closed")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="RAG Chatbot API for Physical AI Textbook",
        lifespan=lifespan,
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Register routes
    app.include_router(health.router, prefix="/health", tags=["Health"])
    app.include_router(chat.router, prefix="/chat", tags=["Chat"])

    # Root endpoint
    @app.get("/")
    async def root() -> dict[str, str]:
        """Root endpoint with service information."""
        return {
            "service": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "operational",
        }

    return app


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register global exception handlers.

    Args:
        app: FastAPI application instance
    """

    @app.exception_handler(ChatbotException)
    async def chatbot_exception_handler(
        request: Request, exc: ChatbotException
    ) -> JSONResponse:
        """Handle custom chatbot exceptions."""
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        if isinstance(exc, type) and hasattr(exc, "__name__"):
            exc_type = exc.__name__
        else:
            exc_type = type(exc).__name__

        # Determine appropriate status code
        if "RateLimit" in exc_type:
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
        elif "Validation" in exc_type or "NoResults" in exc_type:
            status_code = status.HTTP_400_BAD_REQUEST

        response_data = {
            "error": exc_type,
            "message": exc.message,
        }

        # Add retry_after if available
        if hasattr(exc, "retry_after"):
            response_data["retry_after"] = exc.retry_after

        # Add details if in debug mode
        if settings.DEBUG and exc.details:
            response_data["details"] = exc.details

        return JSONResponse(
            status_code=status_code,
            content=response_data,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle request validation errors."""
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": "ValidationError",
                "message": "Invalid request format",
                "details": exc.errors(),
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        """Handle HTTP exceptions."""
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "HTTPError",
                "message": exc.detail,
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all unhandled exceptions."""
        logger.exception(f"Unhandled exception: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred" if not settings.DEBUG else str(exc),
            },
        )


# Create application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info",
    )
