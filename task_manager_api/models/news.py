from pydantic import BaseModel
from typing import Optional

class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    published_at: Optional[str] = None