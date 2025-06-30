from datetime import datetime, timezone
from typing import Annotated, Optional

from fastapi import Cookie, Depends
from sqlalchemy import select

from src.auth.models.session import Session
from src.database.service import SessionDep
from src.errors.models import CustomHttpException
from src.users.models.user import User


class GetSessionUser:
    def __init__(self, required: bool):
        self.required = required

    async def __call__(
        self,
        session: SessionDep,
        session_token: str = Cookie(None, alias=Session.KEY_NAME),
    ) -> Optional[User]:
        required = self.required

        if session_token is None:
            if required:
                raise CustomHttpException(
                    status_code=401,
                    detail="Session token is required for this operation.",
                )
            return None

        statement = select(Session).where(Session.token == session_token).limit(2)
        user_session = (await session.scalars(statement)).one_or_none()
        if user_session is None:
            if required:
                raise CustomHttpException(
                    status_code=401,
                    detail="Invalid session token.",
                )
            return None

        if user_session.expires_at < datetime.now(timezone.utc):
            await session.delete(user_session)
            if required:
                raise CustomHttpException(
                    status_code=401,
                    detail="Session token has expired.",
                )
            return None

        user: User = await user_session.awaitable_attrs.user
        return user


get_session_user = GetSessionUser(required=True)
SessionUser = Annotated[User, Depends(get_session_user)]

get_optional_session_user = GetSessionUser(required=False)
OptionalSessionUser = Annotated[Optional[User], Depends(get_optional_session_user)]
