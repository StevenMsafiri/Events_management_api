from app.config import cursor

# create a new event
def create_event(data):
    """Query to create a new event in the table of events"""
    query = """ INSERT INTO events(id, title, description, start_time, end_time, location, email, user) 
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

    try:
        cursor.execute(query, (
        data["id"], data["title"], data["description"], data["start_time"], data["end_time"], data["location"],
        data["email"], data["user"]))

    except Exception as e:
        return f"Failed to create event: {e}"
    finally:
        cursor.connection.commit()
        cursor.close()

# fetch all events
def get_events():
    """Query to get all events in the table of events"""
    query= "SELECT * FROM events"

    try:
        cursor.execute(query)
        events = cursor.fetchall()
        if not events:
            return f"No events found"
        return events

    except Exception as e:
        return f"Failed to get events: {e}"
    finally:
        cursor.connection.commit()
        cursor.close()

# fetch one event
def get_event(id):
    """Query to get a specific event in the table of events"""

    query="SELECT * FROM events WHERE id=%s"

    try:
        cursor.execute(query, (id,))
        event = cursor.fetchone()
        if not event:
            return f"No event found"
        return event
    except Exception as e:
        return f"Failed to get event: {e}"
    finally:
        cursor.connection.commit()
        cursor.close()

