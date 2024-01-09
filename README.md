# Illinois Institute of Technology Course Scheduling Application

## The Team
Marcin Landa, Nadeem Hussein, Robert Soler, Hans Guttormsen, Nabilah Siddiqui

## Problem Statement
Creating a schedule at Illinois Institute of Technology can be a hassle because of the vast amount of class options and requirements. The Illinois Tech Course Scheduling application simplifies the task for students by taking the classes the user has taken and recommending classes that are required and fit their schedule while also containing all the necessary information in one place.

## How It Started
As a group of students that attend IIT, we all had similar problems when it came to registering for classes. A common problem that we found is that it is hard to keep track of requirements, taken classes, available classes and which classes you have already registered for since each of these requires having a different tab open which leads to constantly switching between tabs. We decided to design and program a web application that keeps all this information in one simple spot. Another feature of this application is that it reccomends 5 classes that are available and that are still required for you to take. This application eliminates some of the hassle during registration time and minimizes the need of constant back and forth emails between stuudetns and professors as well as students and their advisor.

## Application Walkthrough
![IIt Image](https://github.com/MarcinLanda/IPRO-IIT-Scheduling-App/raw/main/FlaskReference/static/images/mies_campus.jpg?raw=true "IIt Image")

When you open the application, you are greeted by a login screen which allows you to either login, continue as a guest or create an account. 
![Login Page](https://github.com/MarcinLanda/IPRO-IIT-Scheduling-App/raw/main/FlaskReference/static/images/Page1.png?raw=true "Login Page")

When creating an account, you are required to enter a username and password. There are two fields to enter in your password, the second one is the confirm the password is correct.
![Account Page](https://github.com/MarcinLanda/IPRO-IIT-Scheduling-App/raw/main/FlaskReference/static/images/Page2.png?raw=true "Account Page")

After creating your account, you choose your major from a drop down, currently the application is only available for Computer Science, Computer Engiinering and Computer and Cybersecurity Engineering.
![Major Page](https://github.com/MarcinLanda/IPRO-IIT-Scheduling-App/raw/main/FlaskReference/static/images/Page3.png?raw=true "Major Page")

This takes you to the main part of the application where you get your class recommendations, can see your classes in a list or a calendar and search for and add new classes. This is where users will create their schedules for the next semester using a database of all classes offered in the next semester. 
![Schedule Page](https://github.com/MarcinLanda/IPRO-IIT-Scheduling-App/raw/main/FlaskReference/static/images/Page4.png?raw=true "Schedule Page")

In the profile section of the website, the user is allowed to add all of the classes they have already taken and have the credits for. This allows our application to look at the given major and taken classes and create a list of classes that are still required by the user. On this page there is a table that shows all of the classes taken by the student, each class is seperated by the subject of the class. There is also a table that contains all of the classes remaining to be able to graduate with the given major.
![Profile Page](https://github.com/MarcinLanda/IPRO-IIT-Scheduling-App/raw/main/FlaskReference/static/images/Page5.png?raw=true "Profile Page")

## Next Steps
Although the application mostly works, there is still a lot of work to be done in order for the application to be fully functional. One required task is to host the database and web server publicly instead of locally. Currently for the application to run, the user has to host the database and the website on their personal device. There is also a lot of tweaks that need to be done to ensure all the data is correctly being taken from the website and stored in the database. This will ensure all available classes are shown on our app and make it easier for the reccomendation algorithm to know exactly which classes are eligible for what requirements.
