from fastapi import FastAPI

from ai.router import router as ai_router

app = FastAPI()
app.include_router(ai_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)