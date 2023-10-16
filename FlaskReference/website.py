from flask import Flask, render_template, request, redirect, url_for, jsonify
from jinja2 import Environment
from flask_socketio import SocketIO
from cryptography.fernet import Fernet
import db
from db_oop import student_account, classes, getAllClasses

'''This is where flask application is being made.'''
app = Flask(__name__, template_folder="templates")

key = b'-NwUP8bcuumHeCWIJPz2L_MQimrSxUCKXZaNwYHRbQU='
cipher = Fernet(key)

# Directs to Main Page 
@app.route("/", methods = ['GET', 'POST'])
def home():
    return render_template("login.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")    # renders and executes index.html

@app.route("/major", methods = ['GET', 'POST'])
def major():
    return render_template("major.html")    # renders and executes index.html

@app.route("/redirect_major", methods = ['GET', 'POST'])
def redirect_major():
    name_input = request.form.get("name")
    password_input = request.form.get("pass")
    return render_template("major.html", name = name_input, password = password_input)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    return render_template("login.html")    # renders and executes index.html

@app.route("/courses", methods=['GET'])
def get_courses():
    classJSON = getAllClasses()
    # print(classJSON)
    return classJSON

@app.route("/course_display", methods=['GET'])
def show_classes():
    return render_template("course_display.html")    

# This version of the /result route uses the object-oriented approach for the database entries (see db_test.py)
# Still a work in progress.
@app.route("/result", methods = ['POST', 'GET'])
def result():
    source = request.form.get('source')
    if source == "major":
        name_input = request.form.get("name")          # Extracts the "name" field from the form
        print("name is", name_input)
        password_input = request.form.get("pass")  # Extracts the "name" field from the dictionary
        major_input = request.form.get("major")
        newUser = student_account(un=name_input, pswd=password_input, mjr=major_input) 
        print(newUser.username)
        print(newUser.password)
        newUser.insertToDB()
        #print(newUser.major)
        print('oop is used1')
        return render_template("signup.html",done=True)
    # elif source == "major":
    #     #getting backend api 
    #     print("in major rn")
    #     major_input = request.form.get("major")
    #     newUser.major = major_input
    #     #return render_template("major.html", done=True)
    #     print(newUser.username)
    #     print(newUser.password)
    #     print(newUser.major)
    #     newUser.insertToDB()
    #     if major_input == "true":
    #         return render_template("signup.html", done=True)
    #     else:
    #         return render_template("signup.html", done=True)
    elif source == "login":
        name_input = request.form.get("name")   # Extracts the "name" field from the form
        password_input = request.form.get("pass")  # Extracts the "name" field from the form
        guest_input = request.form.get("guest-input") # Extracts the "name" field from the form
        print("name is ", name_input)
        userInput = student_account(name_input, password_input)
        print(userInput.isInDB())
        if guest_input == "true":
            # Handle the guest user case
            return render_template("major.html", done=True)
        elif userInput.isInDB() is False:
            return "Invalid credentials!"
        else:
            student_db_info = student_account.getFromDB(userInput)
            return render_template("welcome.html", name=student_db_info.username, 
                                          major=student_db_info.major) # renders and executes index.html again,
                                                                        # but this time with the given name
        
           

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')