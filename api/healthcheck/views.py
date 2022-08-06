from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/healthcheck",
    dependencies=[],
    tags=["healthcheck"]
)


class HealthCheckResult(BaseModel):
    status: str
    message: str


@router.get("", response_model=HealthCheckResult)
async def healthcheck(_id: int = None):
    return HealthCheckResult(status="OK", message="Everything is fine")
