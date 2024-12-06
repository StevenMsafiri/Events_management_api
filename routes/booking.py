from flask_restx import Namespace, fields, marshal_with
from services.booking_services import create_booking, cancel_booking, get_user_bookings


bookings_ns = ()