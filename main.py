from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from domain.question import question_router
from domain.answer import answer_router
from domain.user import user_router


app = FastAPI()

origins: list[str] = [
    "http://localhost:5173",
    "http://3.38.35.243:5173",
    "https://3.38.35.243:5173",
]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(question_router.router)
app.include_router(answer_router.router)
app.include_router(user_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))


@app.get(path="/")
async def index() -> FileResponse:
    return FileResponse("frontend/dist/index.html")
