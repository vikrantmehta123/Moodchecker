# Moodchecker
This is a web app built using Flask framework, that follows MVC architechture. The database related functionalities are implemented using Flask-SQLAlchemy.  
The purpose of this app is simple: To make sure that when everyone from the family gets home, they know how the day of other members has been and everybody stays on the same page.

### Features:
- Integrated Google Sign-In
- Uses Google Calendar API to set automated mood reminders on User's calendar
- Uses SMTP to send mood update mails to the user's family.

### How to Run the Application?
- Run the following command `pip install -r requirements.txt` to install the packages required for the application. 
- To enable Google Sign-In and Google Calendar related API, register the application on [Google Console](https://console.cloud.google.com/apis/credentials) and create credentials.
- Configure a Flask-SQLAlchemy database in a file named `config.py`. Also include the Google Client ID, as well as your email credentials to enable mailing functions.
- Upon completion, run the command `python Application/models.py` to create the database.
- After that, run the command `python Application/main.py` to start the application on the local server.

### Issues:
- New reminders are automatically set every 10th day, upon a mood update. So, if a user misses to update his mood on the 10th day, he will not get any reminders until he updates the mood manually.
