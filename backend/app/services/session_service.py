from datetime import datetime

from app.database.mongodb import sessions_collection
from app.core.security import hash_refresh_token

async def create_session(
        user_id: str,
        refresh_token: str,
        expires_at,
        device: str = "unknown"):

    session = {
        "user_id": user_id,
        "refresh_token_hash":
            hash_refresh_token(refresh_token),
        "device": device,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at,
        "revoked": False
    }

    result = await sessions_collection.insert_one(
        session
    )

    return str(result.inserted_id)

async def get_session(
        refresh_token: str):

    return await sessions_collection.find_one(
        {
            "refresh_token_hash":
                hash_refresh_token(
                    refresh_token
                )
        }
    )

async def validate_session(
        refresh_token: str):

    session = await get_session(
        refresh_token
    )

    if not session:
        return None

    if session["revoked"]:
        return None

    if session["expires_at"] < datetime.utcnow():
        return None

    return session

async def revoke_session(
        refresh_token: str):

    return await sessions_collection.update_one(
        {
            "refresh_token_hash":
                hash_refresh_token(
                    refresh_token
                )
        },
        {
            "$set": {
                "revoked": True
            }
        }
    )

async def revoke_all_sessions(
        user_id: str):

    return await sessions_collection.update_many(
        {
            "user_id": user_id,
            "revoked": False
        },
        {
            "$set": {
                "revoked": True
            }
        }
    )

async def get_user_sessions(
        user_id: str):

    sessions = []

    cursor = sessions_collection.find(
        {
            "user_id": user_id
        }
    )

    async for session in cursor:

        sessions.append({
            "id": str(session["_id"]),
            "device": session["device"],
            "created_at":
                session["created_at"],
            "expires_at":
                session["expires_at"],
            "revoked":
                session["revoked"]
        })

    return sessions

async def delete_expired_sessions():

    return await sessions_collection.delete_many(
        {
            "expires_at": {
                "$lt": datetime.utcnow()
            }
        }
    )