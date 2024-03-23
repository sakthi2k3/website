# # web.py

# from flask import Flask, render_template, request
# from chatbot import *

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/chat', methods=['POST'])
# def chat():
#     query = request.form['query']
#     response = ""
#     medicine_name = extract_medicine_name(query)
#     if ' and ' in medicine_name or ',' in medicine_name:
#         medicine_names = extract_medicine_names(medicine_name)
#         if medicine_names:
#             for medicine_name in medicine_names:
#                 response += "\n"
#                 chat_response = chat_with_bot(medicine_name)
#                 if not chat_response:
#                     response += f"Could not extract medicine name from the query: {medicine_name}\n"
#                 else:
#                     if "side effects" in query or "side effect" in query:
#                         side_effects = ', '.join(chat_response['side_effects'])
#                         response += f"Side Effects of {chat_response['medicine']}: {side_effects}\n"

#                     if "substitutes" in query or "substitute" in query or "alternative" in query:
#                         substitutes = ', '.join(chat_response['substitute'])
#                         response += f"Alternative medicines for {chat_response['medicine']}: {substitutes}\n"

#                     if "use" in query or "uses" in query:
#                         uses = ', '.join(chat_response['uses'])
#                         response += f"{chat_response['medicine']} is commonly used for: {uses}\n"
#         else:
#             response = "Could not extract medicine names from the query."
#     else:
#         chat_response = chat_with_bot(medicine_name)
#         if chat_response:
#             if "side effects" in query or "side effect" in query:
#                 side_effects = ', '.join(chat_response['side_effects'])
#                 response += f"Side Effects of {chat_response['medicine']}: {side_effects}\n"

#             if "substitutes" in query or "substitute" in query or "alternative" in query:
#                 substitutes = ', '.join(chat_response['substitute'])
#                 response += f"Alternative medicines for {chat_response['medicine']}: {substitutes}\n"

#             if "use" in query or "uses" in query:
#                 uses = ', '.join(chat_response['uses'])
#                 response += f"{chat_response['medicine']} is commonly used for: {uses}\n"
#         else:
#             response = "Could not extract medicine name from the query."

#     return render_template('index.html', query=query, response=response)




# if __name__ == "__main__":
#     app.run(debug=True)


# web.py

# web.py

from flask import Flask, render_template, request, redirect, url_for
from chatbot import *
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials, db
from extract import extract
import json
app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("medloc-dd7ae-firebase-adminsdk-zuqmf-010684f38f.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://medloc-dd7ae-default-rtdb.firebaseio.com/'
})

# Get a database reference
ref = db.reference('/pharmacies')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('registration.html')

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    data = {
        "owner_name": request.form['owner_name'],
        "owner_email": request.form['owner_email'],
        "owner_phone": request.form['owner_phone'],
        "owner_password": request.form['owner_password'],
        "pharmacy_name": request.form['pharmacy_name'],
        "address": request.form['address'],
        "latitude": request.form['latitude'],
        "longitude": request.form['longitude'],
        "opening_hours": request.form['opening_hours']
    }

    # Extract medicine details from uploaded file
    uploaded_file = request.files['database_file']
    if uploaded_file:
        # Save the uploaded file
        uploaded_file_path = 'uploaded_file.xlsx'
        uploaded_file.save(uploaded_file_path)

        # Extract medicine details
        medicine_details = extract(uploaded_file_path)
        if medicine_details:
            # Add medicine details to the data dictionary
            data['medicine_details'] = medicine_details
        else:
            return "Error: Failed to extract medicine details from the uploaded file."

    try:
        # Convert data dictionary to JSON format
        json_data = json.dumps(data)

        # Push JSON data to Firebase under "pharmacies" node
        ref.push(json_data)
        return "Registration successful. Data updated to Firebase."
    except Exception as e:
        return f"Error: {e}"


@app.route('/chatbot')
def chatbot():
     return render_template('chatbot.html')
@app.route('/chat', methods=['POST'])
def chat():
    query = request.form['query']
    response = ""
    medicine_name = extract_medicine_name(query)
    if ' and ' in medicine_name or ',' in medicine_name:
        medicine_names = extract_medicine_names(medicine_name)
        if medicine_names:
            for medicine_name in medicine_names:
                response += "\n"
                chat_response = chat_with_bot(medicine_name)
                if not chat_response:
                    response += f"Could not extract medicine name from the query: {medicine_name}\n"
                else:
                    if "side effects" in query or "side effect" in query:
                        side_effects = ', '.join(chat_response['side_effects'])
                        response += f"Side Effects of {chat_response['medicine']}: {side_effects}\n"

                    if "substitutes" in query or "substitute" in query or "alternative" in query:
                        substitutes = ', '.join(chat_response['substitute'])
                        response += f"Alternative medicines for {chat_response['medicine']}: {substitutes}\n"

                    if "use" in query or "uses" in query:
                        uses = ', '.join(chat_response['uses'])
                        response += f"{chat_response['medicine']} is commonly used for: {uses}\n"
        else:
            response = "Could not extract medicine names from the query."
    else:
        chat_response = chat_with_bot(medicine_name)
        if chat_response:
            if "side effects" in query or "side effect" in query:
                side_effects = ', '.join(chat_response['side_effects'])
                response += f"Side Effects of {chat_response['medicine']}: {side_effects}\n"

            if "substitutes" in query or "substitute" in query or "alternative" in query:
                substitutes = ', '.join(chat_response['substitute'])
                response += f"Alternative medicines for {chat_response['medicine']}: {substitutes}\n"

            if "use" in query or "uses" in query:
                uses = ', '.join(chat_response['uses'])
                response += f"{chat_response['medicine']} is commonly used for: {uses}\n"
        else:
            response = "Could not extract medicine name from the query."

    return render_template('chatbot.html', query=query, response=response)

if __name__ == "__main__":
    app.run(debug=True)
