from typing import List, Optional
from pydantic import BaseModel

class Organizer(BaseModel):
    name: str
    email: str


class Joiner(BaseModel):
    name: str
    email: str
    country: str


class Event(BaseModel):
    id: Optional[int]
    name: str
    date: str
    organizer: Organizer
    status: str
    type: str
    location: str
    max_attendees: int
    joiners: Optional[List[Joiner]]
