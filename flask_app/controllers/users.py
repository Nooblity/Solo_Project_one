from flask_app import app
from flask import Flask, render_template, request, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User


bcrypt = Bcrypt(app)

@app.route('/')         
def index():
    return render_template('index.html')

@app.route('/regipage')         
def registpage():
    return render_template('registration.html')

@app.route('/loginpage')         
def loginpage():
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    if not User.validate_user(request.form):
        return redirect ('/')
    # validate the form here ...
    # create the hash
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    # put the pw_hash into the data dictionary
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "address": request.form['address'],
        "zip": request.form['zip'],
        "city": request.form['city'],
        "state": request.form['state'],
        "password" : pw_hash
    }
    # Call the save @classmethod on User
    user_id = User.save(data)
    # store user id into session
    session['users_id'] = user_id
    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        # if we get False after checking the password
        flash("Invalid Email/Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['users_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")

@app.route('/dashboard')
def success():
    if 'users_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['users_id']
    }    
    return render_template ("dashboard.html", user=User.get_user_by_id(data),receipes=Receipe.get_all())

@app.route('/logout')         
def destory_session():
    session.clear()
    return redirect("/")


