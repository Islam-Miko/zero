from fastapi import FastAPI, Request


def get_application():
    app = FastAPI()
    return app


app = get_application()


@app.get("/")
async def te_route(request: Request):
    return {
        "status_code": 200,
        "message": "ok"
    }
