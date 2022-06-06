from pydantic import BaseModel


class TwitterTrend(BaseModel):
    name: str
    tweet_volume: int = None
