from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Pizza:
    db = "pizza"
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.crust = data['crust']
        self.size = data['size']
        self.cheese = data['cheese']
        self.topping1 = data['topping1']
        self.topping2 = data['topping2']
        self.topping3 = data['topping3']
        self.price = data['price']
        
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO pizza (name,size,crust,cheese,topping1, topping2,topping3,price) VALUES (%(name)s,%(size)s,%(crust)s,%(cheese)s,%(topping1)s,%(topping2)s,%(topping3)s,%(price)s );'
        return connectToMySQL(cls.db).query_db(query,data)    