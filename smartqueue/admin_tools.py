# smartqueue/admin_tools.py

from smartqueue.db import SessionLocal, Admin, Booking, Location
from .utils import check_admin, send_sms
from datetime import datetime


def admin_dashboard(location_name, username, password):
    """Display all bookings for a location."""
    admin = check_admin(username, password)
    if not admin:
        print(" Invalid credentials.")
        return

    session = SessionLocal()
    location = session.query(Location).filter_by(name=location_name).first()
    if not location:
        print(f" Location '{location_name}' not found.")
        session.close()
        return

    bookings = session.query(Booking).filter_by(location_id=location.id).all()
    if not bookings:
        print(f"No bookings for {location_name}.")
    else:
        print(f" Bookings for {location_name}:")
        for b in bookings:
            print(f"ID: {b.id}, Name: {b.patient_name}, Priority: {b.priority}, Status: {b.status}")
    session.close()

def process_next(location, username, password):
    """Mark the next user in queue as served."""
    admin = check_admin(username, password)
    if not admin:
        print("Invalid credentials.")
        return

    session = SessionLocal()
    next_booking = (
        session.query(Booking)
        .filter_by(location=location, status="waiting")
        .order_by(Booking.priority.desc(), Booking.created_at)
        .first()
    )

    if not next_booking:
        print("No users to process.")
    else:
        print(f"Processing next user: {next_booking.name} (ID: {next_booking.id})")
        next_booking.status = "completed"
        session.add(next_booking)
        session.commit()
        print("User has been marked as completed.")
    session.close()

def analytics(location_name, username, password):
    """Show basic analytics for a location."""
    admin = check_admin(username, password)
    if not admin:
        print(" Invalid credentials.")
        return

    session = SessionLocal()
    location = session.query(Location).filter_by(name=location_name).first()
    if not location:
        print(f"Location '{location_name}' not found.")
        session.close()
        return

    bookings = session.query(Booking).filter_by(location_id=location.id).all()
    total = len(bookings)
    priority_count = {"normal": 0, "priority": 0, "emergency": 0}

    for b in bookings:
        if b.priority in priority_count:
            priority_count[b.priority] += 1

    print(f" Analytics for {location_name}:")
    print(f"Total bookings: {total}")
    for k, v in priority_count.items():
        print(f"{k.capitalize()} bookings: {v}")
    session.close()


def list_locations(username, password):
    """List all locations where bookings exist."""
    admin = check_admin(username, password)
    if not admin:
        print(" Invalid credentials.")
        return

    session = SessionLocal()
    locations = session.query(Location).all()
    if not locations:
        print("No locations found.")
    else:
        print(" Available locations:")
        for loc in locations:
            print(f"- {loc.name}")
    session.close()


def notify(location_name, username, password, async_send=False, count=1):
    """Notify the next user(s) in line for a location."""
    admin = check_admin(username, password)
    if not admin:
        print(" Invalid credentials.")
        return

    session = SessionLocal()
    location = session.query(Location).filter_by(name=location_name).first()
    if not location:
        print(f" Location '{location_name}' not found.")
        session.close()
        return

    next_bookings = (
        session.query(Booking)
        .filter_by(location_id=location.id, status="waiting")
        .order_by(Booking.priority.desc(), Booking.created_at)
        .limit(count)
        .all()
    )

    if not next_bookings:
        print("No users to notify.")
    else:
        for b in next_bookings:
            message = f"Hello {b.patient_name}, your turn is coming up at {location_name}!"
            if getattr(b, "phone", None):
                if async_send:
                    send_sms(b.phone, message)
                else:
                    send_sms(b.phone, message)
            print(f" Notified {b.patient_name} (ID: {b.id})")
            b.statu
