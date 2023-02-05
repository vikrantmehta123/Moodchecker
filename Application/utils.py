from datetime import datetime, timedelta

# region Google Sign-In Functions
def verify_google_login(token):
    """
    Upon a Google Sign-In, returns the idinfo returned by Google
    """

    from google.oauth2 import id_token
    from google.auth.transport import requests 
    from main import app   

    # Verify the token, and return the response
    idinfo = id_token.verify_oauth2_token(token, requests.Request(), app.CLIENT_ID, clock_skew_in_seconds=5)
    return idinfo

def get_userinfo(google_response):
    user = {}
    if "given_name" in google_response:
        user['given_name'] = google_response["given_name"]
    if "family_name" in google_response:
        user["last_name"] = google_response["family_name"]
    if "email" not in google_response:
        raise Exception("Email not given")
    user['email'] = google_response["email"]
    return user
# endregion Google Sign-In Functions

# region Google Calendar API Functions
def create_recurring_event(holiday, time):
    recurrence_rule = create_recurrence_rule(holiday)
    dateTime = create_dateTime(time)
    print(f"dateTime is {dateTime}")
    event = {
        'summary': 'Mood Update',
        'description': "Let others know of your mood here: http://localhost:8080/moods",
        'start': {
            'dateTime': f'{dateTime}',
            'timeZone': "Asia/Kolkata"
        },
        'end': {
            'dateTime': f'{dateTime}',
            'timeZone': "Asia/Kolkata"
        },
        'recurrence': [
            f"{recurrence_rule}"
        ],
        "reminders": {
            "useDefault" : False,
            "overrides" : [
                {
                    "method" : "popup",
                    "minutes" : 30
                }
            ]
        }
    }
    print(f"Recurrence rule is:{recurrence_rule}")
    return event

def create_recurrence_rule(holiday):
    byday = get_byday(holiday)
    end_day = datetime.today() + timedelta(10)
    month = end_day.month
    day = end_day.day
    if month < 10:
       month = f"0{month}" 
    if day < 10:
        day = f"0{day}"
    end_day = f"{end_day.year}{month}{day}" 
    rule = f"RRULE:FREQ=DAILY;UNTIL={end_day};BYDAY={byday}"
    return rule

def get_byday(holiday):
    if holiday == 6:
        return "MO,TU,WE,TH,FR,SA"
    elif holiday == 0:
        return "TU,WE,TH,FR,SA,SU"
    elif holiday == 1:
        return "WE,TH,FR,SA,SU,MO"
    elif holiday == 2:
        return "TH,FR,SA,SU,MO,TU"
    elif holiday == 3:
        return "FR,SA,SU,MO,TU,WE"
    elif holiday == 4:
        return "SA,SU,MO,TU,WE,TU"
    else:
        return "SU,MO,TU,WE,TU,FR"

def create_dateTime(time):
    today = datetime.today()
    return datetime(today.year, today.month, today.day, time.hour, time.minute, time.second).isoformat("T")
    
# endregion Google Calendar API Functions

# region Validators
def validate_email_address(email_address) -> bool:
    """Performs a validation check on email of user"""
    import re
    pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.match(pat,email_address):
        return True
    else:
        return False
    
def validate_first_name(name) -> bool:
    """Performs a basic validation check on the first name of a user"""
    if name.replace(" ", "").isalpha():
        return True
    else:
        return False
# endregion Validators

# region Email Functions

import smtplib
import os 
from email.message import EmailMessage

EMAIL = os.environ.get('My_email')
PASSWORD = os.environ.get('My_email_password')

def mood_converter(mood):
    if mood == 0:
        return "Sad"
    elif mood == 1:
        return "Neutral"
    else:
        return 'Happy'

def send_auth_email(recipients):
    """ Sends the verification mail to everyone in the list. Returns all the emails which threw an error."""

    body = \
    """
    Dear Moodchecker Member, 
    Please consent to the permission to edit and create calendar events. We require this permission to send you reminders for your mood update.
    Please use this link to provide authorization: http://localhost:8080/auth

    Regards, 
    Team Moodchecker
    """
    msg = EmailMessage()
    msg['Subject'] = 'Authorization Email'
    msg['From'] = EMAIL
    msg.set_content(body)
    errorMails = [ ]
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL, PASSWORD)
        for member in recipients:
            try:
                msg['TO'] = member.email
                smtp.send_message(msg)
                del msg['TO']
            except smtplib.SMTPRecipientsRefused:
                errorMails.append(member)
                del msg["TO"]
                continue
        smtp.quit()
    return

def send_mood_update(person, mood, recipients):
    body = \
    f"""
    Greetings!
    A family member has just updated his today's mood. {person} is feeling {mood}. 
    Be sure to be consider their mood when they come home.
    """
    msg = EmailMessage()
    msg['Subject'] = 'Mood Update'
    msg['From'] = EMAIL
    msg.set_content(body)
    errorMails = [ ]
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL, PASSWORD)
        for member in recipients:
            try:
                msg['TO'] = member.email
                smtp.send_message(msg)
                del msg['TO']
            except smtplib.SMTPRecipientsRefused:
                errorMails.append(member)
                del msg["TO"]
                continue
        smtp.quit()
# endregion Email Functions
