from main import app
from flask import render_template, request, session, redirect, make_response, abort, url_for, flash
from Models.models import *
from Application.utils import *

CLIENT_ID = app.CLIENT_ID
app = app.app


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register/<int:admin_status>", methods=["GET", "POST"])
def register(admin_status):
    if request.method == "GET":
        flash("Please make sure you provide an email id that is linked with Google Calendar")
        response = make_response(render_template("register.html"))
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        return response
    else:

        # Check if the admin has registered or not
        if admin_status == 0:

            # Step 1: Handling the CSRF issues
            csrf_token_cookie = request.cookies.get('g_csrf_token')
            if not csrf_token_cookie:
                abort(400, 'No CSRF token in Cookie.')
            csrf_token_body = request.form['g_csrf_token']
            if not csrf_token_body:
                abort(400, 'No CSRF token in post body.')
            if csrf_token_cookie != csrf_token_body:
                abort(400, 'Failed to verify double submit cookie.')

            # Step 2: Handling the Google's ID Token
            token = request.form["credential"]

            # Verify the token
            admin = google_login_authentication(token)
            if admin:
                admin_status = 1
                return redirect(url_for("register", admin_status=1))
            else:
                return "There was an error with the login"
        else:
            # If admin has registerd already, enter the data to database
            if 'admin' in session:
                # TODO: Enter the data to the database, and send a mail to all the users for authorization of Google calendar
                flash("We will need to add a reminder to Google Calendar, which requires your permission. \nPlease authorize this by using the mail id provided.")
                pass
            return render_template("register.html")

@app.route("/moods", methods=["GET", "POST"])
def moods():
    if request.method == "GET":
        if 'user' not in session:
            session["next_url"] = "moods"
            return redirect(url_for("login"))
        return render_template("moods.html")
    else:
        pass
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # TODO: Implement logic for checking whether the logged in user is a valid admin or a regular user, and set the keys accordingly
        token = request.form["credential"]
        admin = google_login_authentication(token)
        if admin:
            session['admin'] = admin
        else:
            return "There was an error with the login"

        # Redirect users to appropriate page
        if 'next_url' in session:
            return redirect(url_for(session["next_url"]))
        else:
            return "Some unknown error occurred"

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if 'admin' not in session:
        session["next_url"] = "login"
        return redirect(url_for('login'))
    if request.method == "GET":
        # TODO: Implement a function to get family members of from the data
        members = []
        return render_template("edit.html", members=members)
    elif request.method == "POST":
        # TODO: Implement a function to update the database for the changes in entries
        pass

@app.route("/reports", methods=["GET","POST"])
def reports():
    if 'admin' not in session:
        session["next_url"] = "reports"
        return redirect(url_for('login'))

    if request.method == "GET":
        # TODO: Implemnt a function to get the last month's data
        report = []
        return render_template("reports.html", report= report)


@app.route("/auth")
def auth():
    import os.path

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import Flow

    SCOPES = "openid https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = Flow.from_client_secrets_file(
                "D:\Moodchecker\credentials.json",
                scopes=SCOPES,
                redirect_uri="http://localhost:8080/handle_response")
            auth_uri, state = flow.authorization_url(access_type='offline', prompt="login", include_granted_scopes='true')
            session['state'] = state
            return redirect(auth_uri)


@app.route("/handle_response")
def handle_response():
    if session:
        if request.args.get('state', '') != session['state']:
            abort('CSRF Attack warning!')
            
        from google_auth_oauthlib.flow import Flow
        from googleapiclient.discovery import build

        SCOPES = "openid https://www.googleapis.com/auth/calendar.events https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        if 'code' in request.args:
            code = request.args.get("code")
            flow = Flow.from_client_secrets_file(
                    "D:\Moodchecker\credentials.json",
                    scopes=SCOPES,
                    redirect_uri="http://localhost:8080/handle_response")
            flow.fetch_token(code=code)
            credentials = flow.credentials
            return "access granted"
        else:
            return "access denied"
    else:
        return "some unknown error occurred"
