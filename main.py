from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.routers import field, general, websockets

app = FastAPI()
app.include_router(general.router)
app.include_router(field.router)
app.include_router(websockets.router)

templates = Jinja2Templates(directory="src/templates")

origins = ["https://multi-minesweeper-9a0a1.web.app",
           "http://multi-minesweeper-9a0a1.web.app",
           "http://localhost:3000"]

app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_methods=["*"], allow_headers=["*"])


@app.get("/")
def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


register_tortoise(app,
                  db_url="sqlite://database/minesweeper.sql",
                  modules={"models": ["src.models.db"]},
                  generate_schemas=True,
                  add_exception_handlers=True)
if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0')
