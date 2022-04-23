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
        query = 'INSERT INTO pizzas (name,size,crust,cheese,topping1, topping2,topping3) VALUES (%(name)s,%(size)s,%(crust)s,%(cheese)s,%(topping1)s,%(topping2)s,%(topping3)s);'        
        return connectToMySQL(cls.db).query_db(query,data)
    
    def get_total(cls):
        query = 'Select  (sizes.price + topping1.price + topping2.price + topping3.price) as total from pizzas \
                left outer join toppings as topping1 on topping1 = topping1.name  \
                left outer join toppings as topping2 on topping2 = topping2.name \
                left outer join toppings as topping3 on topping3 = topping3.name\
                left outer join sizes on pizzas.size = sizes.size\
                where id = (SELECT MAX(ID) FROM pizzas)'
        total = connectToMySQL(cls.db).query_db(query)
        return total
    
    # def update_price(cls,total):
    #     query = "UPDATE pizzas SET price= %(total)s where id = (SELECT MAX(ID) FROM pizzas);"
    #     return connectToMySQL(cls.db).query_db(query,total)    
    
    def get_one (cls):
        query = "Select pizzas.size as size, cheese, crust, topping1,  topping2, topping3,  (sizes.price + topping1.price + topping2.price + topping3.price) as total from pizzas \
                left outer join toppings as topping1 on topping1 = topping1.name  \
                left outer join toppings as topping2 on topping2 = topping2.name \
                left outer join toppings as topping3 on topping3 = topping3.name\
                left outer join sizes on pizzas.size = sizes.size\
                where id = (SELECT MAX(ID) FROM pizzas)"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        pizza = connectToMySQL(cls.db).query_db(query)
        return pizza
    
class Order:
    db = "pizza"
    def __init__( self , data ):
        self.id = data['id']
        self.user_id = data['users_id']
        self.price = data['total_price'] 
    
    @classmethod    
    def save(cls, data):
        query = 'INSERT INTO pizzas (user_id,total_price) VALUES (%(user_id)s,%(total)s);'        
        return connectToMySQL(cls.db).query_db(query,data)    
        