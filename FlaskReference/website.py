from flask import Flask, render_template, request, redirect, url_for, Markup, jsonify
from jinja2 import Environment
from flask_socketio import SocketIO
from cryptography.fernet import Fernet
import db

app = Flask(__name__)
socket = SocketIO(app)
database = dict()
key = b'-NwUP8bcuumHeCWIJPz2L_MQimrSxUCKXZaNwYHRbQU='
cipher = Fernet(key)

@socket.on('message')
def handle_msg(message):
    print("I have received: ", message)
    info = cipher.decrypt(message)
    print("Real message: ", info)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods = ['GET'])
def signup():
    return render_template("signup.html")    # renders and executes index.html


@app.route("/login", methods = ['GET'])
def login():
    return render_template("login.html")    # renders and executes index.html


@app.route("/result", methods = ['POST', 'GET'])
def result():
    source = request.form.get('source')
    print(database)

    if source == "signup":
        name_input = request.form.get("name")          # Extracts the "name" field from the form
        print("name is", name_input)
        password_input = request.form.get("pass")  # Extracts the "name" field from the dictionary
        db.newEntry(name_input, password_input)
        return "Account Created"

    elif source == "login":
        name_input = request.form.get("name")   # Extracts the "name" field from the form
        password_input = request.form.get("pass")  # Extracts the "name" field from the form
        print("name is ", name_input)
        if db.searchEntry(name_input) is False:
            return "Invalid credentials!"
        else:
            db_pass = db.getEntry(name_input)
            print("password is", db_pass)
            if db_pass != password_input:
                return "Invalid credentials!!"
            else:
                return Markup(render_template("welcome.html", name=name_input,
                                       password=password_input))  # renders and executes index.html again,
                                                           # but this time with the given name


name = "trina"
print(db.getEntry(name))

# Create an endpoint to receive JSON data
@app.route('/receive-json-list', methods=['POST'])
def receive_json():
    try:
        # Get the JSON data from the request
        json_data_list = request.get_json()

        # Process each JSON object in the list
        processed_data = []

        for json_data in json_data_list:
            name = json_data.get('Name')
            major = json_data.get('Major')
            # Perform actions with the received JSON data
            # ...
            # Add the processed data to the result
            processed_data.append({"Name": name, "Major": major})
            # Return a JSON response with the processed data
            response_data = {
                "status": "success",
                "message": "JSON list received and processed successfully",
                "data": processed_data,
            }
            print(json_data_list)
            return jsonify(json_data_list), 200

    except Exception as e:
        # Handle exceptions if necessary
        response_data = {
            "status": "error",
            "message": str(e),
        }
        return jsonify(response_data), 500


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    socket.run(app, debug=True)
