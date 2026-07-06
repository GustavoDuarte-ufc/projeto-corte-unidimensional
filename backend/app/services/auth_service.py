from datetime import datetime, timedelta

from app.database.mongodb import users_collection

from app.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    hash_password,
    REFRESH_TOKEN_EXPIRE_DAYS
)

from app.services.session_service import (
    create_session
)


async def create_user(user):

    existing_user = await users_collection.find_one(
        {"email": user.email}
    )

    if existing_user:
        return None

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hash_password(user.password),
        "role": "user",
        "active": True,
        "failed_attempts": 0,
        "locked_until": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = await users_collection.insert_one(
        new_user
    )

    return str(result.inserted_id)


async def login_user(user):

    db_user = await users_collection.find_one(
        {"email": user.email}
    )

    if not db_user:
        return None

    valid = verify_password(
        user.password,
        db_user["password"]
    )

    if not valid:
        return None

    payload = {
        "sub": str(db_user["_id"]),
        "email": db_user["email"],
        "role": db_user["role"]
    }

    access_token = create_access_token(
        payload
    )

    refresh_token = create_refresh_token(
        payload
    )

    await create_session(
        user_id=str(db_user["_id"]),
        refresh_token=refresh_token,
        expires_at=datetime.utcnow()
        + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        device="unknown"
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }