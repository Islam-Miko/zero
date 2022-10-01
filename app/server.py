from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.authentication import AuthenticationError
from starlette.middleware.authentication import AuthenticationMiddleware

from app.auth.middleware import JWTAuthentication
from app.auth.routes import router as auth_router
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
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthentication())

    app.include_router(users_router)
    app.include_router(auth_router)
    return app


app = get_application()


@app.get("/")
async def te_route(request: Request):
    return {"status_code": 200, "message": "ok", "user": str(request.user)}


@app.get("/routes/")
async def routes():
    return [{"path": route.path, "name": route.name} for route in app.routes]


@app.exception_handler(AuthenticationError)
async def authentication_handler(request: Request, exc: AuthenticationError):
    return JSONResponse(
        content={"message": str(exc)}, status_code=status.HTTP_401_UNAUTHORIZED
    )
