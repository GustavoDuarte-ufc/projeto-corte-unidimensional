from datetime import datetime
from pydantic import BaseModel


class SessionResponse(BaseModel):
    id: str
    device: str
    created_at: datetime
    expires_at: datetime
    revoked: bool