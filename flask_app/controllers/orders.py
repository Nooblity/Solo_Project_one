from flask_app import app
from flask import Flask, render_template, request, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.order import Pizza

@app.route('/customize')         
def customize():
    if 'users_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['users_id']
    }    
    return render_template ("customize.html", user=User.get_user_by_id(data))