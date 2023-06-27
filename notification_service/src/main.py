from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.v1.event_publisher import router
from core.config import settings
from services.publisher import get_rabbitmq, rabbitmq_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbitmq_worker.connect()
    yield
    await rabbitmq_worker.close()


app = FastAPI(
    lifespan=lifespan,
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


app.include_router(router, prefix="/api/v1", tags=["publisher"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
