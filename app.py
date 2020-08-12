#dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

#create flask app
app = Flask(__name__)

#establish mongoDB connection w/ pymongo
mongo = PyMongo (app, uri="mongodb://localhost:27017/mars_app")

#render index.html template using data from Mongo
@app.route("/")
def home():

    #find one record of data from mongoDB
    mars = mongo.db.mars.find_one()

    #return template & data
    return render_template ("index.html", mars = mars)

#trigger scrape fxn
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()

    #update mongoDB using update & upsert
    mongo.db.mars.update({}, mars_data, upsert=True)

    #redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
