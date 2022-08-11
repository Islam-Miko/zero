from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.users.routes import router as users_router


def get_application():
    app = FastAPI()
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    return app


app = get_application()

app.include_router(users_router)


@app.get("/")
async def te_route(request: Request):
    return {
        "status_code": 200,
        "message": "ok"
    }
