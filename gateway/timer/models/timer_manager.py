from pydantic import BaseModel


class TimerManager(BaseModel):
    user_id: str
    task_name: str
