from main import app
from flask import render_template, request, session, redirect, make_response, abort, url_for, jsonify
from Models.models import *
from utils import *

CLIENT_ID = app.CLIENT_ID
app = app.app


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/register/<int:admin_status>", methods=["GET", "POST"])
def register(admin_status):
    if request.method == "GET":
        response = make_response(render_template("register.html"))
        response.headers["Referrer-Policy"] = "no-referrer-when-downgrade"
        return response
    else:
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
            from google.oauth2 import id_token
            from google.auth.transport import requests
            token = request.form["credential"]

            # Verify the token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        
            # If the user is verified by Google, 
            if idinfo["email_verified"]:
                admin = {
                    "first_name" : idinfo["given_name"], 
                    "last_name" : idinfo["family_name"], 
                    "email" : idinfo["email"]
                }
                session['admin'] = admin
                admin_status = 1
                return redirect(url_for("register", admin_status=1))
        else:
            print(request.form.to_dict())
            if 'admin' in session:
                pass
            return render_template("register.html")

@app.route("/moods", methods=["GET", "POST"])
def moods():
    if request.method == "GET":
        return render_template("moods.html")
    
@app.route("/login/<int:sender_code", methods=["GET", "POST"])
def login(sender_code):
    if request.method == "GET":
        return render_template("login.html")
    else:
        # TODO: Implement logic for checking whether the logged in user is a valid admin
        token = request.form["credential"]
        admin = google_login_authentication(token)
        if admin:
            session['admin'] = admin
        else:
            return "There was an error with the login"

        # If the request for login came from the edit page, redirect the user to the edit page
        if sender_code == 2:
            return redirect(url_for("edit"))
        elif sender_code == 3:
            return redirect(url_for('reports'))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if 'admin' not in session:
        return redirect(url_for('login', sender_code=2))
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
        return redirect(url_for('login', sender_code=3))

    if request.method == "GET":
        # TODO: Implemnt a function to get the last month's data
        report = []
        return render_template("reports.html", report= report)