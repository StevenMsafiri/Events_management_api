from flask import request
from flask_restx import Namespace, Resource, fields
from services.event_services import create_event, get_events, get_event, delete_event, update_event

events_ns = Namespace("Event Processes", description="APIs for events related operations")


events_model = events_ns.model("Events", {
    'id':fields.Integer(readOnly=True),
    'title':fields.String(required=True, description='Event title'),
    'description':fields.String(required=True, description='About the event'),
    'start_time':fields.DateTime(required=True, description='Starting time and date'),
    'end_time':fields.DateTime(required=True, description='Ending time and date'),
    'location':fields.String(required=True, description='Location'),
    'email':fields.String(required=True, description='Email')
})

@events_ns.route("/")
class EventsResource(Resource):
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
        return events, 201

@events_ns.route("<int:event_id>")
@events_ns.doc(params={'event_id': fields.Integer()})
class Event(Resource):
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
        email = data.get("email")

        response = update_event(event_id, title, description, start_date, end_date, location, email)
        return response







