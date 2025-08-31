#!/usr/bin/env python3
import argparse
from smartqueue.db import (
    init_db,
    seed_admin,
    seed_locations,
    SessionLocal,
    Admin,
    Booking,
    Location,
    Notification,
)
from smartqueue.queue_manager import book_appointment, check_status, notify_user, process_next
from smartqueue.admin_tools import admin_dashboard, analytics
from smartqueue.queue_manager import reschedule_appointment
from smartqueue.queue_manager import cancel_booking

def list_locations():
    session = SessionLocal()
    locs = session.query(Location).all()
    session.close()
    if locs:
        print("📍 Available locations:")
        for loc in locs:
            print(f"- {loc.name}")
    else:
        print("No locations found.")


def main():
    parser = argparse.ArgumentParser(description="SmartQueue CLI Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Book command
    book_parser = subparsers.add_parser("book", help="Book an appointment")
    book_parser.add_argument("location", help="Location name")
    book_parser.add_argument("username", help="User name")
    book_parser.add_argument(
        "--priority", choices=["normal", "emergency"], default="normal", help="Priority level"
    )

    # Status command
    status_parser = subparsers.add_parser("status", help="Check booking status")
    status_parser.add_argument("username", help="User name")

    # Notify command
    notify_parser = subparsers.add_parser("notify", help="Send notification to a user")
    notify_parser.add_argument("username", help="User name")
    notify_parser.add_argument("message", help="Notification message")

    # Admin dashboard command
    dashboard_parser = subparsers.add_parser("dashboard", help="Show admin dashboard")
    dashboard_parser.add_argument("location", help="Location name")
    dashboard_parser.add_argument("username", help="Admin username")
    dashboard_parser.add_argument("password", help="Admin password")

    #process-next 
    process_parser = subparsers.add_parser("process-next", help="Process the next user in queue")
    process_parser.add_argument("location", help="Location name")
    process_parser.add_argument("username", help="Admin username")
    process_parser.add_argument("password", help="Admin password")


    # Analytics command
    analytics_parser = subparsers.add_parser("analytics", help="Show analytics data")
    analytics_parser.add_argument("location", help="Location name")
    analytics_parser.add_argument("username", help="Admin username")
    analytics_parser.add_argument("password", help="Admin password")

    # reschedule command 
    reschedule_parser = subparsers.add_parser("reschedule", help="Reschedule an existing appointment")
    reschedule_parser.add_argument("location", type=str, help="Location name")
    reschedule_parser.add_argument("patient_name", type=str, help="Patient name")
    reschedule_parser.add_argument("priority", type=str, nargs="?", default="normal", help="New priority (normal/emergency)")
    
    # cancel command
    cancel_parser = subparsers.add_parser("cancel", help="Cancel a booking")
    cancel_parser.add_argument("location", help="Location name")
    cancel_parser.add_argument("patient_name", help="Patient name")


    # Locations command
    subparsers.add_parser("locations", help="List all available locations")

    # Init DB command
    subparsers.add_parser("initdb", help="Initialize the database with default data")

    args = parser.parse_args()

    if args.command == "book":
        result = book_appointment(args.location, args.username, args.priority)
        print(result)

    elif args.command == "status":
        rows = check_status(args.username)
        if rows:
            for r in rows:
                print(f"Booking ID: {r.id}, Location ID: {r.location_id}, Status: {r.status}")
        else:
            print(f"No bookings found for {args.username}.")

    elif args.command == "notify":
        notify_user(args.username, args.message)

    elif args.command == "dashboard":
        admin_dashboard(args.location, args.username, args.password)

    elif args.command == "analytics":
        analytics(args.location, args.username, args.password)


    elif args.command == "locations":
        list_locations()

    elif args.command == "process-next":
        process_next(args.location, args.username, args.password)

    elif args.command == "reschedule":
        print(reschedule_appointment(args.location, args.patient_name, args.priority))

    elif args.command == "cancel":
        print(cancel_booking(args.location, args.patient_name))

    elif args.command == "initdb":
        init_db()
        seed_admin()
        seed_locations()
        print("✅ Database initialized with default admin and locations.")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
