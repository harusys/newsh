from pydantic import BaseModel


class TimerManager(BaseModel):
    id: str
    user_id: str
    task_name: str
    scheduled_at: str
