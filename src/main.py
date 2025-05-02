from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from core import db_helper, settings
from fastapi import FastAPI
from api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan, title="QuickMealAPI")

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.midd.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def ping():
    return {"ping": "pong"}
