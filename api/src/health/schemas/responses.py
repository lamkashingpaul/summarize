from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "ok",
            }
        }
    }
