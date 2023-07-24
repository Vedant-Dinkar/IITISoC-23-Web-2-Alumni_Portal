from flask import Flask, render_template, request, redirect, url_for, session,g
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase
from pymongo import MongoClient
from linkedin_api import Linkedin
from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd
import pymongo 

app = Flask(__name__)
app.config["SECRET_KEY"] = "hjhjsdahhds"
socketio = SocketIO(app)

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


# Connect to MongoDB-----------------------------------------------------------------------

client = MongoClient("mongodb://localhost:27017/")
db = client["_app_"]
messages_collection = db["messages"]
profiles_collection = db["profiles"]  # Create a new collection for storing LinkedIn profiles


# home ----------------------------------------------------------------------------------
@app.route('/')
def index():
    return render_template('compiled.html')

# login------------------------------------------------------------------------------------

@app.route('/login')
def login():
    return render_template('login.html')


# events extension----------------------------------------------------------------------
@app.route('/events.html')
def events():
    return render_template('events.html')


# jobs---------------------------------------------------------------------------------
@app.route('/jobs.html')
def jobs():
    return render_template('jobs.html')


# chat app---------------------------------------------------------------------------------
rooms = {}

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
    
    return code

def get_global_chat_room():
    global_room = "GLOBAL"
    if global_room not in rooms:
        rooms[global_room] = {"members": 0, "messages": []}
    return global_room

def get_rooms_list():
    return list(rooms.keys())

@app.route("/chat.html", methods=["POST", "GET"])
def chat():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("chat.html", error="Please enter a name.", code=code, name=name)

        if join != False and not code:
            return render_template("chat.html", error="Please enter a room code.", code=code, name=name)

        room = code
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
        elif code.upper() == "GLOBAL":
            room = get_global_chat_room()
        elif code not in rooms:
            return render_template("chat.html", error="Room does not exist.", code=code, name=name)

        session["room"] = room
        session["name"] = name
        return redirect(url_for("room"))

    return render_template("chat.html", rooms=get_rooms_list())

@app.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("chat"))

    return render_template("room.html", code=room, messages=rooms[room]["messages"], rooms=get_rooms_list())

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }
    send(content, to=room)
    rooms[room]["messages"].append(content)
    messages_collection.insert_one(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        if room.upper() == "GLOBAL":
            room = get_global_chat_room()
        else:
            leave_room(room)
            return

    join_room(room)
    send({"name": name, "message": "has entered the room"}, to=room)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")


# linkedinapi------------------------------------------------------------------------------

@app.route('/linkedinurl', methods=['GET'])
def linkedinurl():
    return render_template('linkedinurl.html')

@app.route('/get_profile', methods=['POST'])
def get_profile():
    # Authenticate using any LinkedIn account credentials
    api = Linkedin('mralumniportal@gmail.com', 'iitisoc123')

    # Retrieve the profile URL from the request
    profile_url = request.form['profile_url']

    # Parse the profile URL to extract the profile identifier
    profile_id = profile_url.split('/')[-2]

    if len(profile_id) <= 1:
        profile_id = profile_url.split('/')[-1]

    # Get the member's profile
    profile = api.get_profile(profile_id)

    # Extract the information
    location_name = profile.get('locationName')
    first_name = profile.get('firstName')
    last_name = profile.get('lastName')
    headline = profile.get('headline')

    experiences = profile.get('experience', [])
    companies = []
    headlines = []

    for exp in experiences:
        company = exp.get('companyName')
        if company:
            companies.append(company)

        position = exp.get('title')
        if position:
            headlines.append(position)

    # Create a dictionary with the extracted information
    extracted_info = {
        "location_name": location_name,
        "first_name": first_name,
        "last_name": last_name,
        "headline": headline,
        "companies": companies,
        "headlines": headlines
    }

    return redirect(url_for('profile', **extracted_info))

# ---------------------new excel code-----------------------------------------------------------------------
def load_profiles_from_excel(excel_file):
    # Load the existing profiles from the Excel file into a DataFrame
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file, engine="openpyxl")
    else:
        df = pd.DataFrame()
    return df


def profile_exists(profiles_collection, extracted_info):
    # Check if the profile already exists in the MongoDB collection based on specific columns
    existing_profile = profiles_collection.find_one({
        "location_name": extracted_info["location_name"],
        "first_name": extracted_info["first_name"],
        "last_name": extracted_info["last_name"],
        "headline": extracted_info["headline"]
    })

    return existing_profile is not None

@app.route('/profile', methods=['GET'])
def profile():
    extracted_info = {
        "location_name": request.args.get('location_name'),
        "first_name": request.args.get('first_name'),
        "last_name": request.args.get('last_name'),
        "headline": request.args.get('headline'),
        "companies": request.args.getlist('companies'),
        "headlines": request.args.getlist('headlines'),
        # "url": profile_url  # Include the LinkedIn profile URL in the extracted_info dictionary
    }
   # Store the profile information in MongoDB
    if not profile_exists(profiles_collection, extracted_info):
        profiles_collection.insert_one(extracted_info)

        # Save the profile information in an Excel file
        excel_file = "profile_info.xlsx"
        df = load_profiles_from_excel(excel_file)

        # Append the new profile information to the DataFrame
        df = pd.concat([df, pd.DataFrame([extracted_info])], ignore_index=True)

        # Save the DataFrame to the Excel file
        df.to_excel(excel_file, index=False, engine="openpyxl")

    return render_template('profile.html', extracted_info=extracted_info)

if __name__ == "__main__":
    socketio.run(app,port=5000, debug=True)