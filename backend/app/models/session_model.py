from datetime import datetime
from pydantic import BaseModel


class SessionModel(BaseModel):
    user_id: str
    refresh_token_hash: str
    device: str
    created_at: datetime
    expires_at: datetime
    revoked: bool