from flask import Flask, render_template, request, redirect, url_for, jsonify
from jinja2 import Environment
from flask_socketio import SocketIO
from cryptography.fernet import Fernet
import db
from db_oop import student_account

'''This is where flask application is being made.'''
app = Flask(__name__)

key = b'-NwUP8bcuumHeCWIJPz2L_MQimrSxUCKXZaNwYHRbQU='
cipher = Fernet(key)


@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("login.html")


@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")    # renders and executes index.html


@app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template("login.html")    # renders and executes index.html

# This version of the /result route uses the db.py layout. 
# The other version follows the db_test.py layout. They are different.
# @app.route("/result", methods = ['POST', 'GET'])
# def result():
#     source = request.form.get('source')

#     if source == "signup":
#         name_input = request.form.get("name")          # Extracts the "name" field from the form
#         print("name is", name_input)
#         password_input = request.form.get("pass")  # Extracts the "name" field from the dictionary
#         major_input = request.form.get("major")
#         db.newEntry(name_input, password_input, major_input)
#         return render_template("signup.html", done=True)

#     elif source == "login":
#         name_input = request.form.get("name")   # Extracts the "name" field from the form
#         password_input = request.form.get("pass")  # Extracts the "name" field from the form
#         print("name is ", name_input)
#         if db.searchEntry(name_input) is False:
#             return "Invalid credentials!"
#         else:
#             db_pass = db.getEntry(name_input)[1]
#             print("password is", db_pass)
#             if db_pass != password_input:
#                 return "Invalid credentials!!"
#             else:
#                 db_major = db.getEntry(name_input)[2]
#                 return Markup(render_template("welcome.html", name=name_input, major=db_major))  # renders and executes index.html again,
#                                                            # but this time with the given name


# This version of the /result route uses the object-oriented approach for the database entries (see db_test.py)
# Still a work in progress.
@app.route("/result", methods = ['POST', 'GET'])
def result():
    source = request.form.get('source')

    if source == "signup":
        name_input = request.form.get("name")          # Extracts the "name" field from the form
        print("name is", name_input)
        password_input = request.form.get("pass")  # Extracts the "name" field from the dictionary
        major_input = request.form.get("major")
        newUser = student_account(name_input, password_input, major_input)
        newUser.insertToDB()
        print('oop is used')
        return render_template("signup.html", done=True)

    elif source == "login":
        name_input = request.form.get("name")   # Extracts the "name" field from the form
        password_input = request.form.get("pass")  # Extracts the "name" field from the form
        print("name is ", name_input)
        userInput = student_account(name_input, password_input)
        print(userInput.isInDB())
        if userInput.isInDB() is False:
            return "Invalid credentials!"
        else:
            student_db_info = student_account.getFromDB(userInput)
            return render_template("welcome.html", name=student_db_info.username, 
                                          major=student_db_info.major) # renders and executes index.html again,
                                                                        # but this time with the given name

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')