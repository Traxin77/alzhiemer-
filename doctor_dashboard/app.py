from flask import Flask, render_template
from pymongo import MongoClient
import os

app = Flask(__name__)

# Replace <db_password> with your actual password.
MONGO_URI = "mongodb+srv://root:root@cluster0.s42uhev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "alzheimer_db"
COLLECTION_NAME = "responses"

# Connect to the MongoDB Cloud cluster
client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def dashboard():
    # Fetch all documents from the collection
    docs = list(collection.find())
    # Convert ObjectId to string so it can be displayed on the frontend.
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    return render_template('dashboard.html', documents=docs)

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True)
