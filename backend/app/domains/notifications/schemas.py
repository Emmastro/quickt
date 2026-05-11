from datetime import datetime

from pydantic import BaseModel


class NotificationPublic(BaseModel):
    id: int
    type: str
    title: str
    body: str
    data: dict | None
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationListResponse(BaseModel):
    items: list[NotificationPublic]
    total: int
    unread_count: int
