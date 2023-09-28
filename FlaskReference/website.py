from flask import Flask, render_template, request, redirect, url_for, Markup, jsonify
from jinja2 import Environment
from flask_socketio import SocketIO
from cryptography.fernet import Fernet
import db

app = Flask(__name__)

key = b'-NwUP8bcuumHeCWIJPz2L_MQimrSxUCKXZaNwYHRbQU='
cipher = Fernet(key)


@app.route("/", methods = ['GET'])
def home():
    return render_template("home.html")


@app.route("/signup", methods = ['GET'])
def signup():
    return render_template("signup.html")    # renders and executes index.html


@app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template("login.html")    # renders and executes index.html

# This version of the /result route uses the db.py layout. 
# The other version follows the db_test.py layout. They are different.
@app.route("/result", methods = ['POST', 'GET'])
def result():
    source = request.form.get('source')

    if source == "signup":
        name_input = request.form.get("name")          # Extracts the "name" field from the form
        print("name is", name_input)
        password_input = request.form.get("pass")  # Extracts the "name" field from the dictionary
        db.newEntry(name_input, password_input)
        return render_template("signup.html", done=True)

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

# This version of the /result route uses the object-oriented approach for the database entries (see db_test.py)
# Still a work in progress.
# @app.route("/result", methods = ['POST', 'GET'])
# def result():
#     source = request.form.get('source')

#     if source == "signup":
#         name_input = request.form.get("name")          # Extracts the "name" field from the form
#         print("name is", name_input)
#         password_input = request.form.get("pass")  # Extracts the "name" field from the dictionary
#         newUser = db()
#         return render_template("signup.html", done=True)

#     elif source == "login":
#         name_input = request.form.get("name")   # Extracts the "name" field from the form
#         password_input = request.form.get("pass")  # Extracts the "name" field from the form
#         print("name is ", name_input)
#         if db.searchEntry(name_input) is False:
#             return "Invalid credentials!"
#         else:
#             db_pass = db.getEntry(name_input)
#             print("password is", db_pass)
#             if db_pass != password_input:
#                 return "Invalid credentials!!"
#             else:
#                 return Markup(render_template("welcome.html", name=name_input,
#                                        password=password_input))  # renders and executes index.html again,
#                                                            # but this time with the given name


name = "trina"
print(db.getEntry(name))


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
