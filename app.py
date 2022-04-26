from flask import Flask, request, jsonify
from peewee import *

# this allows you to convert from a model to a dictionay and vice versa
from playhouse.shortcuts import model_to_dict, dict_to_model
db = PostgresqlDatabase('restaurants',
                        user='laurat', password='',
                        host='localhost', port=5432)
# we use class to create our models


class BaseModel(Model):
    class Meta:
        database = db
# defining our restaurant model


class Restaurant(BaseModel):
    category = CharField()
    description = CharField()


# connect to our database
db.connect()
# # drop tables restaurant if it exists

db.drop_tables([Restaurant])
# makes a restaurant table in our data base

db.create_tables([Restaurant])
# makes a brand new restaurant to add to the restaurants table

Restaurant(category="Fine Dining",
           description="Formal dress code and fine dining etiquette").save()
Restaurant(category="Casual Dining",
           description="Moderately-priced menus").save()
Restaurant(category="Contemporary Casual",
           description="Modern casual yet trendy atmosphere").save()
Restaurant(category="Family Style",
           description="Food served on large platters for parties to share").save()
Restaurant(category="Fast Casual",
           description="Quality of food and prices are usually higher than fast food but lower than casual dining").save()
Restaurant(category="Fast Food",
           description="Usually a chain and serves standardized meals made of processed food").save()
Restaurant(category="Cafe",
           description="Usually serve coffee, tea, pastries, and small items for breakfast and lunch").save()
Restaurant(category="Buffet",
           description="A selection of food at a fixed price").save()
Restaurant(category="Food Trucks and Concession Stands",
           description="These are normally outdoors at sporting events, fairs, or on city streets").save()
Restaurant(category="Pop-Up Restaurant",
           description="Operates temporarily from a few hours to a few months").save()
Restaurant(category="Ghost Restaurant", description="Delivery only").save()


# __name__ is used to tell flask where it is
app = Flask(__name__)


@app.route('/restaurants/', methods=['GET', 'POST'])
@app.route('/restaurants/<id>', methods=['GET', 'PUT', 'DELETE'])
def endpoint(id=None):
    # get request
    if request.method == 'GET':
        # if there is an id get a specific restaurant
        if id:
            return jsonify(model_to_dict(Restaurant.get(Restaurant.id == id)))
        # else if there is no id get all restaurants
        else:

            restaurantsList = []
            for restaurant in Restaurant.select():
                restaurantsList.append(model_to_dict(restaurant))
            return jsonify(restaurantsList)
    # put request
    if request.method == 'PUT':
        return 'PUT REQUEST'
    # post request, creates a new restaurant
    if request.method == 'POST':
        new_restaurant = dict_to_model(Restaurant, request.get_json())
        new_restaurant.save()
        return jsonify({"success": True})
    # delete request
    if request.method == 'DELETE':
        return 'DELETE REQUEST'


app.run(port=9000, debug=True)
