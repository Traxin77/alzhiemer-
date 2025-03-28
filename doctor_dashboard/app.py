from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb+srv://root:root@cluster0.s42uhev.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DATABASE_NAME = "alzheimer_db"
COLLECTION_NAME = "responses"

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

@app.route('/')
def dashboard():
    patient_name = request.args.get('patient', None)
    
    # Fetch unique patient names
    patient_names = collection.distinct("patient_name")

    # Fetch documents based on the selected patient
    query = {} if not patient_name else {"patient_name": patient_name}
    docs = list(collection.find(query))

    for doc in docs:
        doc['_id'] = str(doc['_id'])

    return render_template('dashboard.html', documents=docs, patient_names=patient_names, selected_patient=patient_name)

if __name__ == '__main__':
    app.run(debug=True)
