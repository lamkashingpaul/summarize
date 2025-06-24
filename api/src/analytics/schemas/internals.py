from pydantic import BaseModel


class CreateRequestLogDto(BaseModel):
    client_ip: str
    method: str
    path: str
    query_params: dict
    request_header: dict
    request_body: dict
    response_status: int
    response_header: dict
    response_body: dict
    duration_ms: float
    error: str
