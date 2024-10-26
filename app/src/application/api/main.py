from fastapi import FastAPI
import uvicorn

from application.api.users.handlers import router as users_router


def create_app():
    app = FastAPI(
        title="Envelope",
        description="Envelope API app",
        version="0.0.1",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=True,
    )
    app.include_router(users_router)
    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="localhost", port=8000)