from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

def get_application():
    app = FastAPI()
    return app


app = get_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def te_route(request: Request):
    return {
        "status_code": 200,
        "message": "ok"
    }
