from typing import Literal, Optional, overload

from argon2 import PasswordHasher
from sqlalchemy import select
from sqlalchemy.exc import MultipleResultsFound, NoResultFound

from src.auth.models.account import Account
from src.database.service import SessionDep
from src.errors.models import CustomDatabaseNotFoundException
from src.users.models.user import User
from src.users.schemas.internals import CreateUserDto


async def save_user(create_user_dto: CreateUserDto, session: SessionDep):
    email = create_user_dto.email
    name = create_user_dto.name
    image_url = create_user_dto.image_url

    password_hasher = PasswordHasher()
    hashed_password = password_hasher.hash(create_user_dto.password)

    user = User(
        email=email,
        name=name,
        image_url=image_url,
        is_email_verified=False,
    )
    session.add(user)
    await session.flush()

    account = Account(
        account_id=str(user.id),
        provider_id="credentials",
        password=hashed_password,
        user_id=user.id,
    )
    session.add(account)

    return user


@overload
async def fetch_user_by_email(
    email: str, session: SessionDep, should_fail: Literal[True]
) -> User: ...
@overload
async def fetch_user_by_email(
    email: str, session: SessionDep, should_fail: Literal[False] = False
) -> Optional[User]: ...
async def fetch_user_by_email(
    email: str, session: SessionDep, should_fail: bool = False
) -> Optional[User]:
    try:
        statement = select(User).where(User.email == email).limit(2)
        users = (await session.scalars(statement)).all()

        if not users or len(users) != 1:
            if should_fail:
                raise CustomDatabaseNotFoundException(
                    message=f"User with email: '{email}' not found"
                )
            return None

        return users[0]

    except (NoResultFound, MultipleResultsFound) as e:
        raise CustomDatabaseNotFoundException(
            message=f"User with email: '{email}' not found"
        ) from e
