# import dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# create route for HTML index page
@app.route("/")
def index():
    # use PyMongo to find "mars" collection in database
    mars = mongo.db.mars.find_one()
    # return HTML template using index.html file
    # use "mars" collection
    return render_template("index.html", mars=mars)

# create scraping route
@app.route("/scrape")
def scrape():
    # access database, scrape using scraping.py script 
    # create new variable pointing to mongo database
    mars = mongo.db.mars
    # create variable to hold scraped data
    # reference scrape_all function in scraping.py
    mars_data = scraping.scrape_all()
    # using data stored in mars_data, update database 
    # create new document if it doesn't already exist
    mars.update({}, mars_data, upsert=True)
    # redirect to index after done scraping
    return redirect('/', code=302)

# run Flask app
if __name__ == "__main__":
   app.run()