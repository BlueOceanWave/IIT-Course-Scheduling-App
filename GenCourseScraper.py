import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

URL = "https://bulletin.iit.edu/courses/"  #the constant url for IIT course site
coursesAZ = requests.get(URL)   #get the html
class_list = []  #list of courses, to be made into JSON file


def scrape(newurl) :
    #Open Chrome
    driver = webdriver.Chrome()
    driver.get(newurl)

    blocks = driver.find_elements(By.CLASS_NAME, "courseblock")
    coursecodes = driver.find_elements(By.CLASS_NAME, "coursecode")
    coursetitles = driver.find_elements(By.CLASS_NAME, "coursetitle")
    courseblockdescs = driver.find_elements(By.CLASS_NAME, "courseblockdesc")
    coursehours = driver.find_elements(By.CLASS_NAME, "hours")

 
    for i in range(len(blocks)) :
        codenum = coursecodes[i].text.split(" ")
        if coursehours[i].text[-1] == "e" :
            hours = "0"
            print(codenum[0])
            print(codenum[1])
            print(hours)
        else :
            hours = coursehours[i].text[-1]
        
        theClass = { "subject": codenum[0], 
                     "coursenum": codenum[1], 
                     "title": coursetitles[i].text,
                     "desc": courseblockdescs[i].text,
                     "hours": hours
                    }
        class_list.append(theClass)


def goThroughEachAttr() :
    for line in coursesAZ.text.splitlines() :  #go through each html line
        if "/courses/" in line and "<li>" in line and not ("courses/\"") in line : #get all  courses (required a bit of hard coding for some edge cases)
            ind = line.find("courses") + 8  #each line is "<li><a href="/courses/___/">blah blah</a></li>"
            endind = ind
            while(not (line[endind] == "/")) :
                endind += 1
            courseType = ""
            for i in range(ind, endind) :
                courseType += line[i]
            newURL = URL + courseType + "/"
            scrape(newURL)
        
goThroughEachAttr() #go through each bulletin subsite

outputFileName = "allCourses.json"  #the name of the file the courses will go
with open(outputFileName, 'w') as json_file:  #export list to JSON file
    json_string = json.dump(class_list, json_file, indent = 4)

'''
JSON:
(term.json)
[
    {
        "subject": ---
        "coursenum": ---
        "title": ---
        "desc": ---
        "hours": ---
    },
    {...
    }
]
'''