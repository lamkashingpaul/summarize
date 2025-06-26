from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    email: str
    name: str
    image_url: str | None = None
    is_email_verified: bool

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "email": "foo@bar.com",
                "name": "Foo Bar",
                "image_url": "https://example.com/image.jpg",
                "is_email_verified": True,
            }
        },
    )


class GetAuthenticatedUserResponse(UserResponse, BaseModel):
    pass
