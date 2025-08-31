from datetime import datetime
from smartqueue.db import SessionLocal, Admin, Booking, Location, Notification

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
    query = session.query(Booking)
    if username:
        query = query.filter(Booking.patient_name == username)
    results = query.order_by(Booking.created_at).all()
    session.close()
    return results


def notify_user(username, message):
    session = SessionLocal()
    from smartqueue.db import Notification
    notification = Notification(message=message)
    session.add(notification)
    session.commit()
    session.close()

    print(f"Notification sent to {username}: {message}")


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
