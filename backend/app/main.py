from fastapi import FastAPI
from .database import engine, Base
from .routers import papers, comments

Base.metadata.create_all(bind = engine)

app = FastAPI(
    title = "PeerReviewChain",
    description = "MVP v0.1.0",
    version = "0.1.0"
)

app.include_router(papers.router)
app.include_router(comments.router)

@app.get("/")
def read_root () :
    return {"message" : "PeerReviewChain MVP 서버가 실행 중입니다."}