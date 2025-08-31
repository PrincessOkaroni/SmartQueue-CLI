from datetime import datetime
from smartqueue.db import SessionLocal, Admin, Booking, Location, Notification
from smartqueue.admin_tools import check_admin

def book_appointment(location_name, patient_name, priority="normal"):
    session = SessionLocal()
    try:
        location = session.query(Location).filter_by(name=location_name).first()
        if not location:
            return f"Location '{location_name}' not found."

        new_booking = Booking(
            location_id=location.id,
            patient_name=patient_name,
            priority=priority,
            status="waiting",
            created_at=datetime.utcnow()
        )
        session.add(new_booking)
        session.commit()
        return f"Booking confirmed for {patient_name} at {location_name} with priority {priority}."
    finally:
        session.close()


def check_status(username=None):
    session = SessionLocal()
    try:
        query = session.query(Booking)
        if username:
            query = query.filter(Booking.patient_name == username)
        results = query.order_by(Booking.created_at).all()
        return results
    finally:
        session.close()


def process_next(location_name, username, password):
    """Mark the next user in queue as served."""
    admin = check_admin(username, password)
    if not admin:
        print("Invalid credentials.")
        return

    session = SessionLocal()
    try:
        location = session.query(Location).filter_by(name=location_name).first()
        if not location:
            print(f"Location '{location_name}' not found.")
            return

        next_booking = (
            session.query(Booking)
            .filter_by(location_id=location.id, status="waiting")
            .order_by(Booking.priority.desc(), Booking.created_at)
            .first()
        )

        if not next_booking:
            print("No users to process.")
        else:
            print(f"Processing next user: {next_booking.patient_name} (ID: {next_booking.id})")
            next_booking.status = "completed"
            session.commit()
            print("User has been marked as completed.")
    finally:
        session.close()

def reschedule_appointment(location_name, patient_name, new_priority="normal"):
    session = SessionLocal()
    try:
        booking = (
            session.query(Booking)
            .join(Location, Booking.location_id == Location.id)
            .filter(Location.name == location_name, Booking.patient_name == patient_name)
            .first()
        )
        if not booking:
            return f"No booking found for {patient_name} at {location_name}."

        booking.priority = new_priority
        booking.updated_at = datetime.utcnow()
        session.commit()
        return f"Booking for {patient_name} at {location_name} has been rescheduled with priority {new_priority}."
    finally:
        session.close()

def cancel_booking(location_name, patient_name):
    session = SessionLocal()
    try:
        booking = (
            session.query(Booking)
            .join(Location, Booking.location_id == Location.id)
            .filter(Location.name == location_name, Booking.patient_name == patient_name)
            .first()
        )
        if not booking:
            return f"No booking found for {patient_name} at {location_name}."

        session.delete(booking)
        session.commit()
        return f"Booking for {patient_name} at {location_name} has been canceled."
    finally:
        session.close()


def notify_user(username, message):
    session = SessionLocal()
    try:
        notification = Notification(message=message)
        session.add(notification)
        session.commit()
        print(f"Notification sent to {username}: {message}")
    finally:
        session.close()


def send_notification(message):
    session = SessionLocal()
    try:
        notification = Notification(message=message)
        session.add(notification)
        session.commit()
        return f"Notification sent: {message}"
    finally:
        session.close()


def list_locations():
    session = SessionLocal()
    try:
        locations = session.query(Location).all()
        return [(loc.id, loc.name) for loc in locations]
    finally:
        session.close()
