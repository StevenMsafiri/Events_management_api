from flask import jsonify

from app.config import create_connection, convert_to_mysql_datetime, mysql_to_iso
import  logging

mydb = create_connection()

# create a new event
def create_event(data):
    """Query to create a new event in the table of events"""
    query = """ INSERT INTO events(id, title, description, start_time, end_time, location, email, user_id)
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

    # Convert ISO datetime strings to MySQL datetime format
    mysql_start_time = convert_to_mysql_datetime(data["start_time"])
    mysql_end_time = convert_to_mysql_datetime(data["end_time"])

    try:
        with mydb.cursor() as cursor:
            cursor.execute(query, (
                data["id"], data["title"], data["description"], mysql_start_time, mysql_end_time, data["location"],
                data["email"], data["user_id"]))
            mydb.commit()
            return f"Event {data['id']} created"
    except Exception as e:
        return f"Failed to create event: {e}"

# fetch all events
def get_events():
    """Query to get all events in the table of events"""
    query= "SELECT * FROM events"
    try:
        with mydb.cursor() as cursor:
            cursor.execute(query)
            events = cursor.fetchall()
            if not events:
                return f"No events found"
            events_list = []
            for event in events:
                event_dict = {
                    "id": event['id'],
                    "title": event['title'],
                    "description": event['description'],
                    "start_time": mysql_to_iso(event["start_time"]),
                    "end_time": mysql_to_iso(event["end_time"]),
                    "location": event["location"],
                    "email": event["email"],
                    "user_id": event["user_id"]
                }
                events_list.append(event_dict)
            return jsonify(events_list)
    except Exception as e:
        return f"Failed to get events: {e}"

# fetch one event
def get_event(event_id):
    """Query to get a specific event in the table of events"""

    query="SELECT * FROM events WHERE id=%s"

    try:
        with mydb.cursor(dictionary=True) as cursor:
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()
            if not event:
                logging.error(f"No event found with id: {event_id}")
                return {'message': 'No event found, Check the event_id'}
            # Convert datetime fields to string for serialization
            event['start_time'] = mysql_to_iso(event['start_time'])
            event['end_time'] = mysql_to_iso(event['end_time'])
            return event

    except Exception as e:
        logging.error(f"Failed to get event: {e}")
        return {'message': 'Failed to get event: {}'.format(e)}



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
    update_query = """UPDATE events SET title=%s,description=%s,start_time=%s, end_time=%s, location=%s, email=%s, user_id=%s  WHERE id=%s"""

    try:
        with mydb.cursor() as cursor:
            cursor.execute(search_query, (event_id,))
            event = cursor.fetchone()
            if not event:
                return f"No event found"
            else:
                cursor.execute(update_query, (new_data["id"], new_data["title"], new_data["description"], new_data["start_time"], new_data["end_time"],
                                              new_data["location"], new_data["email"], new_data["user_id"]))
                mydb.commit()
                return f"Event updated successfully"
    except Exception as e:
        return f"Failed to update event: {e}"








