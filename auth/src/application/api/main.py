from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from application.api.users.handlers import router as users_router


def create_app():
    app = FastAPI(
        title="Envelope",
        description="Envelope API auth",
        version="0.0.1",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        debug=True,
    )
    app.include_router(users_router)

    origins = ["http://localhost:3000", "http://31.129.50.189:8000", "http://31.129.50.189:8001"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["POST", "GET", "PUT", "DELETE"],
        allow_headers=["*"],
    )

    return app


if __name__ == "__main__":
    uvicorn.run(create_app(), host="localhost", port=8000)
