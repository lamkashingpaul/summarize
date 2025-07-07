from typing import Literal, Optional, overload

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy import select

from src.auth.models.account import Account
from src.auth.service import fetch_credentials_account_by_email
from src.database.service import SessionDep
from src.errors.models import (
    CustomDatabaseInternalServerErrorException,
    CustomDatabaseNotFoundException,
)
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
    statement = select(User).where(User.email == email).limit(2)
    users = (await session.scalars(statement)).all()

    if len(users) != 1:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"User with email: '{email}' not found."
            )
        return None

    return users[0]


@overload
async def fetch_authenticated_user(
    email: str, password: str, session: SessionDep, should_fail: Literal[True]
) -> User: ...
@overload
async def fetch_authenticated_user(
    email: str, password: str, session: SessionDep, should_fail: Literal[False] = False
) -> Optional[User]: ...
async def fetch_authenticated_user(
    email: str, password: str, session: SessionDep, should_fail: bool = False
) -> Optional[User]:
    account = await fetch_credentials_account_by_email(email, session, should_fail)
    if not account:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' not found."
            )
        return None

    user: User = await account.awaitable_attrs.user

    password_hasher = PasswordHasher()
    hashed_password = account.password
    if hashed_password is None:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message=f"Credentials account with email '{email}' has no password set."
            )
        return None

    try:
        password_hasher.verify(hashed_password, password)
        if password_hasher.check_needs_rehash(hashed_password):
            account.password = password_hasher.hash(password)
        return user

    except VerifyMismatchError as e:
        if should_fail:
            raise CustomDatabaseNotFoundException(
                message="Invalid email or password."
            ) from e
        return None
    except Exception as e:
        if should_fail:
            raise CustomDatabaseInternalServerErrorException(
                message="An error occurred while verifying the password."
            ) from e
        return None
