from main import app
from flask import render_template, request, session, redirect, make_response, abort, url_for
from Models.models import *

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
                return redirect(request.url, admin_status=1)
        else:
            data = request.form.to_dict()
            print(f"data is {data}")
            print("admin status is not 0")
            if 'admin' in session:
                print(f"session is {session['admin']}")
            return render_template("register.html")

@app.route("/moods", methods=["GET", "POST"])
def moods():
    if request.method == "GET":
        return render_template("moods.html")
    
@app.route("/edit")
def edit():
    return render_template("edit.html")

@app.route("/reports", methods=["GET","POST"])
def reports():
    if request.method == "POST":
        print(request.form.to_dict())
        return render_template("reports.html")