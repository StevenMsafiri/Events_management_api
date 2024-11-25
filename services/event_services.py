from app.config import create_connection


connection = create_connection()
cursor = connection.cursor()

# create a new event
def create_event(data):
    """Query to create a new event in the table of events"""
    query = """ INSERT INTO events(id, title, description, start_time, end_time, location, email, user_id) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        cursor.execute(query, (
        data["id"], data["title"], data["description"], data["start_time"], data["end_time"], data["location"],
        data["email"], data["user"]))
        connection.commit()
    except Exception as e:
        connection.rollback()
        connection.close()
        return f"Failed to create event: {e}"

# fetch all events
def get_events():
    """Query to get all events in the table of events"""
    query= "SELECT * FROM events"

    try:
        cursor.execute(query)
        events = cursor.fetchall()
        connection.commit()
        if not events:
            return f"No events found"
        return events

    except Exception as e:
        connection.rollback()
        cursor.close()
        return f"Failed to get events: {e}"

# fetch one event
def get_event(id):
    """Query to get a specific event in the table of events"""

    query="SELECT * FROM events WHERE id=%s"

    try:
        cursor.execute(query, (id,))
        event = cursor.fetchone()
        connection.commit()
        if not event:
            return f"No event found"
        return event
    except Exception as e:
        connection.rollback()
        cursor.close()
        return f"Failed to get event: {e}"


def delete_event(id):
    """Query to delete an event in the table of events"""
    query="DELETE FROM events WHERE id=%s"

    try:
        cursor.execute(query, (id,))
        connection.commit()
        return f"Event {id} deleted"
    except Exception as e:
        connection.rollback()
        cursor.close()
        return f"Failed to delete event: {e}"

def update_event(id, new_title, new_description, start_date, end_date, new_location, new_email, new_user):
    """Query to get a specific event in the table of events"""
    search_query="SELECT * FROM events WHERE id=%s"

    """Query to update a specific event in the table of events"""
    update_query = """UPDATE events SET title=%s,description=%s,start_time=%s, end_time=%s, location=%s, email=%s, user_id=%s  WHERE id=%s"""

    try:
        cursor.execute(search_query, (id,new_title, new_description, start_date, end_date, new_location, new_email, new_user))
        event = cursor.fetchone()
        if not event:
            return f"No event found"
        else:
            cursor.execute(update_query, ())
            connection.commit()
            return f"Event updated successfully"
    except Exception as e:
        connection.rollback()
        cursor.close()
        return f"Failed to update event: {e}"








