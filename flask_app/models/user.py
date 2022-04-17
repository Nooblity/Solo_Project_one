from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
# model the class after the friend table from our database

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class User:
    db = "pizza"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.address = data['address']
        self.zip = data['zip']
        self.state = data['state']
        self.city = data['city']
        self.email = data['email']
        self.phone = data['phone']
        self.preferrence = data['order_preference.orders_id']
        self.password = data['password']        
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name,last_name,email,password,phone, address,city, state, zip) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s ,%(phone)s  ,%(address)s  ,%(city)s   ,%(state)s  ,%(zip)s       );'
        return connectToMySQL(cls.db).query_db(query,data)
    
    
    @classmethod
    def get_all_user(cls):
        query = "SELECT * FROM users;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL(cls.db).query_db(query)
        # Create an empty list to append our instances
        users = []
        # Iterate over the db results and create instances of friends with cls.
        for user in results:
            users.append( cls(user) )
        return users
    
    

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
        
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            is_valid = False
        flash("Email already reigstered, please login", "register")                               
        if len(user['first_name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters.","register")
        if len(user['last_name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters.","register") 
        if not EMAIL_REGEX.match(user['email']):
            is_valid = False 
            flash("Invalid email address!","register")                                                               
        if len(user['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters.","register")
        if user['password'] != user["confirm_password"]:
            is_valid = False
            flash("Password not matched","register")
        return is_valid

    
    
    @classmethod
    def get_user_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])