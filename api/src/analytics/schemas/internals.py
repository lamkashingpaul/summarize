from pydantic import BaseModel, Field


class CreateRequestLogDto(BaseModel):
    client_ip: str = Field(..., min_length=1, max_length=45)
    method: str = Field(..., min_length=1, max_length=10)
    path: str = Field(..., min_length=1, max_length=255)
    query_params: dict = Field(...)
    request_header: dict = Field(...)
    request_body: dict = Field(...)
    response_status: int = Field(...)
    response_header: dict = Field(...)
    response_body: dict = Field(...)
    duration_ms: float = Field(...)
    error: str = Field(..., min_length=0)
