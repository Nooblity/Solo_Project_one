from flask_app import app
from flask import Flask, render_template, request, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from flask_app.models.user import User
from flask_app.models.order import Pizza, Order

@app.route('/customize')         
def customize():
    if 'users_id' not in session:
        return redirect('/logout')
    user_in_session ={
        'id': session['users_id']
    }    
    return render_template ("customize.html", user=User.get_user_by_id(user_in_session))



@app.route('/customizepizza', methods=['POST'])         
def customizepizza():
    pizza = {
        "size":request.form['size'],
        "name":request.form['name'],
        "crust": request.form['crust'],
        "cheese": request.form['cheese'],
        "topping1": request.form['topping1'],
        "topping2": request.form['topping2'],
        "topping3": request.form['topping3'],
    }
    Pizza.save(pizza)
    return redirect("/add_to_order")

@app.route('/add_to_order') 
def add_to_order():
    user_in_session ={
        'id': session['users_id']
    }   
    return render_template ("orders.html", user=User.get_user_by_id(user_in_session),pizzas=Pizza.get_one(Pizza))


# @app.route('/place_order',methods=['POST']) 
# def place_order():
#     data = {
#         "user_id":session['users_id'],
#         "total": request.form['total']
#     }
#     Order.save(data)
#     return redirect("/check_out")