from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from retriever.api import retrieval_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(retrieval_router)


@app.get("/health-check", status_code=200)
def health_check():
    return {"status": "ok"}
