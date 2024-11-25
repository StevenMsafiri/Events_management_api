from asyncio import Event
from flask import request
from flask_restx import Namespace, Resource, fields
from sqlalchemy.sql.coercions import expect

from services.event_services import create_event, get_events, get_event, delete_event, update_event

events_ns = Namespace("Event Processes", description="APIs for events related operations")


events_model = events_ns.model("Events", {
    'id':fields.Integer(readOnly=True),
    'title':fields.String(required=True, description='Event title'),
    'description':fields.String(required=True, description='About the event'),
    'start_date':fields.DateTime(required=True, description='Starting time and date'),
    'end_date':fields.DateTime(required=True, description='Ending time and date'),
    'location':fields.String(required=True, description='Location'),
    'user_id':fields.Integer(required=True, description='User id'),
})

@events_ns.route("/")
class Events(Resource):
    @events_ns.expect(events_model)
    @events_ns.response(201, 'Event successfully created.')
    @events_ns.response(400, 'Bad request.')
    def post(self):
        """Create a new event."""
        data = request.json
        response = create_event(data)
        return response

    def get(self):
        """Get all events."""
        events = get_events()
        return events, 200

@events_ns.route("<int:event_id>")
@events_ns.doc(params={'event_id': fields.Integer()})
class Events(Resource):
    @events_ns.marshal_with(events_model)
    def get(self, event_id):
        """Get a specific event using the event id"""
        event = get_event(event_id)
        return event

    def delete(self, event_id):
        """Delete a specific event using the event id"""
        response = delete_event(event_id)
        return response

    @events_ns.expect(events_model)
    def put(self, event_id):
        """Update a specific event using the event id"""
        data = request.json
        title = data.get("title")
        description = data.get("description")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        location = data.get("location")
        user_id = data.get("user_id")
        email = data.get("email")

        response = update_event(event_id, title, description, start_date, end_date, location, user_id, email)
        return response







