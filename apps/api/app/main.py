from fastapi import FastAPI
from app.api.v1.routers import health, auth, sessions
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="FocusMate API (Phase 1)")

    @app.on_event("startup")
    async def startup_event():
        # Placeholder for startup tasks (DB connect tests etc.)
        pass

    app.include_router(health.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1")

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=settings.APP_HOST, port=int(settings.APP_PORT), reload=True)
