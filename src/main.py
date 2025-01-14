from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER

from core.models import Base, db_helper
from api_v1 import router as router_v1
from src.core.config import settings

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)


@app.get('/')
async def main(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})

@app.post('/new_link')
async def new_link(request: Request, name: str = Form(...)):
    print(name)
    return RedirectResponse(url=app.url_path_for('main'), status_code=HTTP_303_SEE_OTHER)


if __name__ == '__main__':
    uvicorn.run("main:app", port=7890)
