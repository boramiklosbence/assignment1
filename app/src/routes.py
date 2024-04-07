from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from src.file_storage import EventFileManager

# Initialize router
router = APIRouter()

# Endpoint to get all events
@router.get("/events", response_model=List[Event])
async def get_all_events():
    return EventFileManager.read_events_from_file()

# Endpoint to filter events based on criteria
@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(
    date: str = None, organizer: str = None, status: str = None, event_type: str = None
):
    data = EventFileManager.read_events_from_file()

    filtered_data = list(
        filter(
            lambda e: (date is None or e["date"] == date)
            and (organizer is None or e["organizer"]["name"] == organizer)
            and (status is None or e["status"] == status)
            and (event_type is None or e["type"] == event_type),
            data,
        )
    )

    return filtered_data

# Endpoint to retrieve event by ID
@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    data = EventFileManager.read_events_from_file()

    searched_event = next((e for e in data if e["id"] == event_id), None)

    if searched_event:
        return searched_event
    else:
        raise HTTPException(status_code=404, detail="Event not found")

# Endpoint to create a new event
@router.post("/events", response_model=Event)
async def create_event(event: Event):
    data = EventFileManager.read_events_from_file()

    searched_event = next((e for e in data if e["id"] == event.id), None)

    if searched_event:
        raise HTTPException(status_code=400, detail="Event ID already exists")
    else:
        data.append(event.dict())
        EventFileManager.write_events_to_file(data)
        return event

# Endpoint to update an existing event
@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    data = EventFileManager.read_events_from_file()

    searched_event = next((e for e in data if e["id"] == event_id), None)

    if searched_event:
        data[data.index(searched_event)] = event.dict()
        EventFileManager.write_events_to_file(data)
        return event
    else:
        raise HTTPException(status_code=404, detail="Event not found")

# Endpoint to delete an event by its ID
@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    data = EventFileManager.read_events_from_file()

    searched_event = next((e for e in data if e["id"] == event_id), None)

    if searched_event:
        data.remove(searched_event)
        EventFileManager.write_events_to_file(data)
        return {"message": "Event deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Event not found")

# Endpoint to retrieve joiners attending multiple meetings
@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    data = EventFileManager.read_events_from_file()

    joiners = [joiner["name"] for event in data for joiner in event["joiners"]]
    joiners_attending_multiple_meetings = [joiner for joiner in set(joiners) if joiners.count(joiner) >= 2]

    if joiners_attending_multiple_meetings:
        return joiners_attending_multiple_meetings
    else:
        return {"message": "No joiners attending at least 2 meetings"}
