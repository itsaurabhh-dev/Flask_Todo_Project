from flask import jsonify,Flask,render_template,request,redirect,url_for
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import json
import os

app = Flask(__name__)



#Creating A MONGO DB Atlas CONNECTION
load_dotenv()
MONGO_URI = os.getenv('MONGO_URI')
print(MONGO_URI)
uri = MONGO_URI
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

db=client.test
collection = db['Flask-learning']


# creating a API Route
@app.route("/api")
def api(): 
    with open("backend/data.json", "r") as file: 
        data = json.load(file) 
    return jsonify({ "source": "JSON FILE", "data": data })


# to enter Detail 
@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email :
            return render_template("login.html",error = "Please, enter all the value.")
        
        try:
            result = collection.insert_one({
                "name" : name,
                "email" : email,
                "password" : password
            })
            
            return redirect(url_for("success"))
          

        except Exception as e:
            return render_template("login.html",error = f"Database error: {str(e)}")
    
    return render_template("login.html")

@app.route ('/success')
def success():
    return render_template("success.html")            

@app.route("/submittodoitem", methods=["POST"])
def submit():
    item = {
        "itemName": request.form["itemName"],
        "itemDescription": request.form["itemDescription"]
    }

    collection.insert_one(item)

    return "Saved Successfully"


if __name__ =='__main__':
    app.run(debug=True)