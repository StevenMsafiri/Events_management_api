from app.date_conversions import convert_to_mysql_datetime, mysql_to_iso
from app.db_config import create_connection
import  logging

mydb = create_connection()
# print(mydb.database,"WHAT I GET HERE!!")
# create a new event
def create_event(data):
    """Query to create a new event in the table of events"""
    query = """ INSERT INTO events(id, title, description, start_time, end_time, location, email)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

    # Convert ISO datetime strings to MySQL datetime format
    mysql_start_time = convert_to_mysql_datetime(data["start_time"])
    mysql_end_time = convert_to_mysql_datetime(data["end_time"])

    try:
        with mydb.cursor() as cursor:
            cursor.execute(query, (
                data["id"], data["title"], data["description"], mysql_start_time, mysql_end_time, data["location"],
                data["email"]))
            mydb.commit()
            return f"Event {data['id']} created"
    except Exception as e:
        return f"Failed to create event: {e}"

# fetch all events
def get_events():
    """Query to get all events in the table of events."""
    query = "SELECT * FROM events"
    try:
        with mydb.cursor() as cursor:
            cursor.execute(query)
            events = cursor.fetchall()

            if not events:
                return {"message": "No events found", "events": []}, 200

            events_list = []
            for event in events:
                event_dict = {
                    "id": event[0],
                    "title": event[1],
                    "description": event[2],
                    "start_time": mysql_to_iso(event[3]),
                    "end_time": mysql_to_iso(event[4]),
                    "location": event[5],
                    "email": event[6],
                }
                events_list.append(event_dict)

            return {"message": "Success", "events": events_list}, 200

    except Exception as e:
        print(f"Error fetching events: {e}")
        return {"error": f"Failed to get events: {str(e)}"}, 500

# Fetch one item
def get_event(event_id):
    """Query to get a specific event in the table of events."""

    query = "SELECT * FROM events WHERE id=%s"

    try:
        # Use a dictionary cursor to fetch the event as a dict
        with mydb.cursor() as cursor:
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()

            if not event:
                logging.error(f"No event found with id: {event_id}")
                return {'message': 'No event found, check the event_id'}, 404

            # Manually map event data since dictionary cursor is removed
            event_dict = {
                "id": event[0],
                "title": event[1],
                "description": event[2],
                "start_time": mysql_to_iso(event[3]),
                "end_time": mysql_to_iso(event[4]),
                "location": event[5],
                "email": event[6]
            }

            return event_dict, 200

    except Exception as e:
        logging.error(f"Failed to get event: {e}")
        return {'message': f'Failed to get event: {str(e)}'}, 500


def delete_event(id):
    """Query to delete an event in the table of events"""
    query="DELETE FROM events WHERE id=%s"

    try:
        with mydb.cursor() as cursor:
            cursor.execute(query, (id,))
            mydb.commit()
            return f"Event {id} deleted"
    except Exception as e:
        mydb.rollback()
        return f"Failed to delete event: {e}"

def update_event(event_id, new_data):
    """Query to get a specific event in the table of events"""
    search_query="SELECT * FROM events WHERE id=%s"


    """Query to update a specific event in the table of events"""
    update_query = """UPDATE events SET title=%s,description=%s,start_time=%s, end_time=%s, location=%s, email=%s WHERE id=%s"""

    try:
        with mydb.cursor() as cursor:
            cursor.execute(search_query, (event_id,))
            event = cursor.fetchone()
            if not event:
                return f"No event found"
            else:
                # Convert datetime fields if they exist
                start_time = mysql_to_iso(new_data.get("start_time"))
                end_time = mysql_to_iso(new_data.get("end_time"))

                cursor.execute(update_query, (new_data["title"], new_data["description"],start_time, end_time,
                                              new_data["location"], new_data["email"], event_id))
                mydb.commit()
                return {"message": "Event updated successfully", "status": "success"}, 200
    except Exception as e:
        return {"message": f"Failed to update event: {str(e)}", "status": "error"}, 500



get_events()
