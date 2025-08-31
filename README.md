# SmartQueue CLI

SmartQueue is a command-line application for queue management, providing features like booking, status checks, queue analytics, and optional SMS notifications using Twilio. It is built with Python, SQLAlchemy, and Passlib for secure admin management.

# Features

 Book Slots: Patients can book slots with priority levels (normal, priority, emergency).

Queue Management: Admins can process next users and manage queues easily.

Real-Time Notifications: Optional SMS notifications for upcoming turns (via Twilio).

Analytics Dashboard: Provides insights like average waiting time and peak hours.

Authentication: Admin authentication with secure password hashing.

Locations Management: Supports multiple hospitals/locations.

# Technologies Used

Python 3.10+

SQLAlchemy – Database ORM

SQLite – Default database engine

Passlib (bcrypt) – Secure password hashing

Tabulate – Pretty table formatting for CLI

Twilio – SMS notification service (optional)

Colorama – CLI color styling


# Installation

1. Clone the Repository
git clone `https://github.com/PrincessOkaroni/SmartQueue-CLI`

2. Create & Activate Virtual Environment
`python3 -m venv venv`
 `source venv/bin/activate`   

3. Install Dependencies
`pip install -r requirements.txt`

Dependencies

sqlalchemy==2.0.30

tabulate==0.9.0

passlib[bcrypt]==1.7.4

twilio==9.2.3

colorama==0.4.6


# Configuration
Database

SmartQueue uses SQLite by default. The DB file (smartqueue.db) will be created automatically.

Environment Variables (Optional for Twilio)

Create a .env file or set in your shell:

TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_FROM_NUMBER=+1234567890

# Usage

Run the CLI script from the project root:

python smartqueue.py [command] [options]

Available Commands
User Commands

Book a spot in the queue

`python3 -m smartqueue.manage book "CityHospital" "Alex" --priority emergency` 
- priority can be either normal or emergency


Check status

`python3 -m smartqueue.manage status "Alice"`
- check status using username

Cancel booking

`python3 -m smartqueue.manage cancel "CityHospital" "Alex"`


Reschedule

`python3 -m smartqueue.manage reschedule "CityHospital" "Alex" "emergency"`

Admin Dashboard
`python3 -m smartqueue.manage dashboard "CityHospital" "Purity" "2008"`

List all locations

`python3 -m smartqueue.manage locations`


Process next user

`python3 -m smartqueue.manage process-next "CityHospital" "Purity" "2008"`


Send notifications (optional Twilio)

`python3 -m smartqueue.manage notify "CityHospital" "Alex"`


Analytics

`python3 -m smartqueue.manage analytics "CityHospital" "Purity" "2008"`



# Author
Name : Okaroni Purity 
Github: `https://github.com/PrincessOkaroni`
screenrecord link `https://www.loom.com/share/5caba503d5d74ba8a96b1ab23f180953?sid=785c25a5-311b-40af-b404-2dcd274db18b`

# License

MIT License 