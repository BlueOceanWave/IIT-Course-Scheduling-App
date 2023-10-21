from flask import Flask, render_template, request, redirect, url_for, jsonify
from jinja2 import Environment
from flask_socketio import SocketIO
from cryptography.fernet import Fernet
import db
from db_oop import student_account, classes, getAllClasses
import search

'''This is where flask application is being made.'''
app = Flask(__name__, template_folder="templates")

key = b'-NwUP8bcuumHeCWIJPz2L_MQimrSxUCKXZaNwYHRbQU='
cipher = Fernet(key)

# Directs to Main Page 
@app.route("/", methods = ['GET', 'POST'])
def login():
    return render_template("login.html")

@app.route("/signup", methods = ['GET', 'POST'])
def signup():
    return render_template("signup.html")      

@app.route("/home/<username>/<major>", methods = ['GET', 'POST'])
def home(username, major):
    return render_template("welcome.html", name=username, major=major)   

@app.route("/courses", methods=['GET'])
def get_courses():
    classJSON = getAllClasses()
    # print(classJSON)
    return classJSON

@app.route("/course_display", methods=['GET'])
def show_classes():
    return render_template("course_display.html")   

@app.route("/search_course", methods = ["POST"])
def search_course():
    sQuery = request.form.get('query')
    result =  search.show_search_results(sQuery)
    return result

@app.route("/view_profile", methods = ["POST"])
def view_profile():
    usrname = request.form.get('name')
    return render_template("profile.html", name=usrname)

@app.route("/guest_major", methods = ['GET', 'POST'])
def guest_major():
    return render_template("major.html", guest=True)    

@app.route("/redirect_major", methods = ['GET', 'POST'])
def redirect_major():
    name_input = request.form.get("name")
    password_input = request.form.get("pass")
    return render_template("major.html", name = name_input, password = password_input, guest=False)

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
        isGuest = request.form.get('guest')
        newUser = student_account(un=name_input, pswd=password_input, mjr=major_input) 
        print(newUser.username)
        print(newUser.password)
        print(newUser.major)
        print(type(isGuest))
        if isGuest != "True":    # if not guest, then add account to database
            newUser.insertToDB()
            return render_template("signup.html",done=True)
        else:                   # if guest, then send straight to welcome page without adding to database
            return redirect(url_for('home', username="Guest", major=newUser.major))
    elif source == "login":
        name_input = request.form.get("name")   # Extracts the "name" field from the form
        password_input = request.form.get("pass")  # Extracts the "name" field from the form
        guest_input = request.form.get("guest-input") # Extracts the "name" field from the form
        print("name is ", name_input)
        userInput = student_account(name_input, password_input)
        print(userInput.isInDB())
        if userInput.isInDB() is False:
            return "Invalid credentials!"
        else:
            student_db_info = student_account.getFromDB(userInput)
            return redirect(url_for("home", username=student_db_info.username, 
                                          major=student_db_info.major)) # renders and executes index.html again,
                                                                        # but this time with the given name
        

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')