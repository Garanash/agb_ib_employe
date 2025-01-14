from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from core.models import Base, db_helper
from api_v1 import router as router_v1
from src.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router_v1, prefix=settings.api_v1_prefix)

@app.get('/')
async def main():
    return {'status_code': 200}


if __name__ == '__main__':
    uvicorn.run("main:app", port=7890)
