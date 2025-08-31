# smartqueue/utils.py

from smartqueue.db import SessionLocal, Admin

def check_admin(username, password):

    #Validate admin credentials.
    #Returns the Admin object if valid, otherwise None.

    session = SessionLocal()
    admin = session.query(Admin).filter_by(username=username).first()
    session.close()
    if admin and admin.password_hash == password:  # Replace with proper hash check if needed
        return admin
    return None

def send_sms(phone, message):

    #Simulate sending an SMS message.
    
    print(f"Sending SMS to {phone}: {message}")
