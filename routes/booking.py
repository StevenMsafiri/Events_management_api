from  flask import request
from flask_restx import Namespace, fields, Resource

from services.booking_services import create_booking, get_user_bookings, cancel_booking


bookings_ns = Namespace("Booking Services", description="Api routes related to bookings")


create_booking_model = bookings_ns.model("New Booking", {
    "id": fields.Integer(readOnly=True),
    "user_id": fields.Integer(Required=True),
    "event_id": fields.Integer(required=True)
})

booking_model = bookings_ns.model("New Booking", {
    "booking_id": fields.Integer(readOnly=True),
    "event_title": fields.String(readOnly=True),
    "start_time": fields.String(readOnly=True),
    "end_time": fields.String(readOnly=True),
    "location": fields.String(readOnly=True)
})

bookings_response_model = bookings_ns.model('User Bookings', {
    'bookings': fields.List(fields.Nested(booking_model))
})


@bookings_ns.route("/")
class Bookings(Resource):
    @bookings_ns.expect(create_booking_model)
    def post(self):
        """Create a new booking"""
        data = request.json
        booking = create_booking(data)
        return booking

@bookings_ns.route("/<int:user_id>")
@bookings_ns.param("user_id", "The booker's id")
class Booking(Resource):
    @bookings_ns.marshal_with(bookings_response_model)
    def get(self, user_id):
        """Gets all bookings for a specific user"""
        bookings = get_user_bookings(user_id)
        return bookings

@bookings_ns.route("/<int:booking_id>")
@bookings_ns.param("booking_id", "The booking id")
class Booking(Resource):
    def delete(self, booking_id):
        """Deletes a  specific booking"""
        result = cancel_booking(booking_id)
        return result