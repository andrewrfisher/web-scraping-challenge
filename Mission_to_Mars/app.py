# Import Dependencies 
from flask import Flask, render_template, redirect 
from flask_pymongo import PyMongo
import scrape_mars
from splinter import Browser

# Create an instance of Flask app
app = Flask(__name__)

#Use flask_pymongo to set up connection through mLab
#app.config["MONGO_URI"] = os.environ.get('authentication')
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that shows index.html template and finds documents from mongo
@app.route("/")
def home(): 

    # Find data
    mars_info = mongo.db.mars_info.find_one()
    print(mars_info)
    # Return template and data
    return render_template("index.html", mars_info=mars_info)
    

# Route that will trigger scrape function
@app.route("/scrape")
def scrape(): 

    # Run scraped functions
    mars_info = mongo.db.mars_info
    mars_data = scrape_mars.scrape_mars_news()
    #mars_image = scrape_mars.scrape_mars_image()
    mars_facts = scrape_mars.scrape_mars_facts()
    mars_hem = scrape_mars.scrape_mars_hemispheres()
    ##
    mars_info.update({}, mars_data, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__": 
    app.run(debug= True)
