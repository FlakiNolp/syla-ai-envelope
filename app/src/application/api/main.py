from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from application.api.users.handlers import router as users_router
from application.api.chats.handlers import router as chats_router
from application.api.messages.handler import router as messages_router


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
    app.include_router(chats_router)
    app.include_router(messages_router)

    origins = ["*"]

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