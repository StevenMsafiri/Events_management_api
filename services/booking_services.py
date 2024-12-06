from xxlimited_35 import error

from mysql.connector.django import validation

from app.config import create_connection

mydb = create_connection()


def validate_user_and_event(user_id, event_id):
    """Ensures user and event exist before booking"""
    user_query = """SELECT id FROM users WHERE id = %s"""
    event_query = """SELECT id FROM events WHERE id = %s"""


    with mydb.cursor() as cursor:
        cursor.execute(user_query, (user_id,))
        user = cursor.fetchone()
        cursor.execute(event_query, (event_id,))
        event = cursor.fetchone()
        if not user:
            return {'error': 'User does not exist'}, 404
        if not event:
            return {'error': 'Event does not exist'}, 404
        return None


def create_booking(data):
    """Creates a booking for sn event using a specific user"""

    query = """INSERT INTO bookings (user_id, event_id) VALUES (%s, %s)"""

    validation_error = validate_user_and_event(data['user_id'], data['event_id'])
    if validation_error:
        return validation_error

    try:
        with mydb.cursor() as cursor:
            cursor.execute(query, (data['user_id'], data['event_id']))
            mydb.commit()
            return {'message': 'Booking created successfully'}, 201

    except Exception as e:
        if "Duplicate entry" in str(e):
            return {'message': 'Booking already exists'}, 409
        mydb.rollback()
        return {'message': f'Failed to create booking: str(e)'}, 404

def get_user_bookings(user_id):
    """Fetch all bookings for a specific user"""
    query = """SELECT b.id, e.title, e.start_time, e.end_time, e.location FROM bookings b
    JOIN events e ON b.event_id = e.id
    WHERE b.user_id = %s"""

    try:
        with mydb.cursor() as cursor:
            cursor.execute(query, (user_id,))
            bookings = cursor.fetchall()

            if not bookings:
                return {'message': 'No bookings found'}, 404

            bookings_list = [
                {
                    "booking_id": booking[0],
                    "event_title": booking[1],
                    "start_time": booking[2],
                    "end_time": booking[3],
                    "location": booking[4],
                }
                for booking in bookings
            ]

            return {"bookings": bookings_list}

    except Exception as e:
        return {'message': f'Failed to get bookings: {str(e)}'}, 500

def cancel_booking(booking_id):
    """Deletes a booking"""
    query = "DELETE FROM bookings WHERE id = %s"

    try:
        with mydb.cursor() as cursor:
            cursor.execute(query, (booking_id,))
            mydb.commit()
            return {'message': 'Booking deleted successfully'}, 201
    except Exception as e:
        mydb.rollback()
        return {'message': f'Failed to cancel booking: {str(e)}'}, 400

