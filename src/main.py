from contextlib import asynccontextmanager
from src.core import db_helper, settings
from fastapi import FastAPI
from src.api import api_router
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan, title="QuickMealAPI")

app.include_router(api_router)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=settings.midd.cors_allowed_origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@app.get("/")
async def ping():
    return {"ping": "pong"}


if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
