from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn

from api.v1.event_publisher import router
from core.config import settings
from services.publisher import get_rabbitmq


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event('startup')
def startup():
    rabbitmq_publisher = get_rabbitmq()
    rabbitmq_publisher.connect()


@app.on_event("shutdown")
def shutdown():
    rabbitmq = get_rabbitmq()
    rabbitmq.close()


app.include_router(router, prefix="/api/v1", tags=["publisher"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
