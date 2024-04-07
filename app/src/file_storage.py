import json


class EventFileManager:
    FILE_PATH = "events.json"

    def read_events_from_file():
        try:
            with open(f"app/src/{EventFileManager.FILE_PATH}", "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"The file 'app/src/{EventFileManager.FILE_PATH}' does not exist.")
            return []

    def write_events_to_file(events):
        with open(f"app/src/{EventFileManager.FILE_PATH}", "w") as file:
            json.dump(events, file)
