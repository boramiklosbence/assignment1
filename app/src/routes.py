from fastapi import APIRouter, HTTPException
from typing import List
from .models import Event
from src.file_storage import EventFileManager

# Initialize router
router = APIRouter()


# Endpoint to get all events
@router.get("/events", response_model=List[Event])
async def get_all_events():
    # Retrieve all events from the file
    return EventFileManager.read_events_from_file()


# Endpoint to filter events based on criteria
@router.get("/events/filter", response_model=List[Event])
async def get_events_by_filter(
    date: str = None, organizer: str = None, status: str = None, event_type: str = None
):
    # Retrieve all events from the file
    data = EventFileManager.read_events_from_file()

    # Filter events based on provided criteria
    searched_events = list(
        filter(
            lambda e: (date is None or e["date"] == date)
            and (organizer is None or e["organizer"]["name"] == organizer)
            and (status is None or e["status"] == status)
            and (event_type is None or e["type"] == event_type),
            data,
        )
    )

    return searched_events


# Endpoint to retrieve event by ID
@router.get("/events/{event_id}", response_model=Event)
async def get_event_by_id(event_id: int):
    # Retrieve all events from the file
    data = EventFileManager.read_events_from_file()

    # Search for event with the specified ID
    searched_event = next((e for e in data if e["id"] == event_id), None)

    if searched_event:
        return searched_event
    else:
        # Return HTTP 404 error if event not found
        raise HTTPException(status_code=404, detail="Event not found")


# Endpoint to create a new event
@router.post("/events", response_model=Event)
async def create_event(event: Event):
    # Retrieve all events from the file
    data = EventFileManager.read_events_from_file()

    # Check if event ID already exists
    searched_event = next((e for e in data if e["id"] == event.id), None)

    if searched_event:
        # Return HTTP 400 error if event ID already exists
        raise HTTPException(status_code=400, detail="Event ID already exists")
    else:
        # Add new event to the data and write to file
        data.append(event.dict())
        EventFileManager.write_events_to_file(data)
        return event


# Endpoint to update an existing event
@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: int, event: Event):
    # Retrieve all events from the file
    data = EventFileManager.read_events_from_file()

    # Search for event with the specified ID
    searched_event = next((e for e in data if e["id"] == event_id), None)

    if searched_event:
        # Update existing event with new data and write to file
        data[data.index(searched_event)] = event.dict()
        EventFileManager.write_events_to_file(data)
        return event
    else:
        # Return HTTP 404 error if event not found
        raise HTTPException(status_code=404, detail="Event not found")


# Endpoint to delete an event by its ID
@router.delete("/events/{event_id}")
async def delete_event(event_id: int):
    # Retrieve all events from the file
    data = EventFileManager.read_events_from_file()

    # Search for event with the specified ID
    searched_event = next((e for e in data if e["id"] == event_id), None)

    if searched_event:
        # Remove event from data and write to file
        data.remove(searched_event)
        EventFileManager.write_events_to_file(data)
        return {"message": "Event deleted successfully"}
    else:
        # Return HTTP 404 error if event not found
        raise HTTPException(status_code=404, detail="Event not found")


# Endpoint to retrieve joiners attending multiple meetings
@router.get("/events/joiners/multiple-meetings")
async def get_joiners_multiple_meetings():
    # Retrieve all events from the file
    data = EventFileManager.read_events_from_file()

    # Extract names of joiners attending multiple meetings
    joiners = [joiner["name"] for event in data for joiner in event["joiners"]]
    joiners_attending_multiple_meetings = [joiner for joiner in set(joiners) if joiners.count(joiner) >= 2]

    if joiners_attending_multiple_meetings:
        return joiners_attending_multiple_meetings
    else:
        return {"message": "No joiners attending at least 2 meetings"}
