import uvicorn
from starlette.middleware.cors import CORSMiddleware
from core import settings
from create_app import create_app
from api import api_router


main_app = create_app()

main_app.include_router(api_router)
main_app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.midd.cors_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@main_app.get("/")
async def ping():
    return {"ping": "pong"}


if __name__ == "__main__":
    uvicorn.run(main_app)
