import requests
import time
import itertools
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

#https://ssb.iit.edu/bnrprd/bwckctlg.p_disp_course_detail?cat_term_in=202430&subj_code_in=MATH&crse_numb_in=474

URL1 = "https://ssb.iit.edu/bnrprd/bwckctlg.p_disp_course_detail?cat_term_in=202430&subj_code_in=" #course subject would go here (ie CS)
URL2 = "&crse_numb_in=" #course number would go here (ie 480)
req_list = []  #list of courses prereqs, to be made into JSON file
index = 0

'''
Subject : CS 
Course # : 480 
Pre-Subject	: MATH
Pre-Course # : 474	
Other : if placement test or not #I think if there is less than 3 when split "\n" its a placement test, o.w. None
Concurrent : TRUE/FALSE
Min Grade : C
Index : int to keep track of "and"s
'''
def parsereq(req, subject, coursenum) :
    try :
        global index
        presubject = "None"
        precourse = "None"
        other = "None"
        concurrent = "False"
        mingrade = "None"
        pieces = req.split("\n")
        cleanpieces = []
        for piece in pieces :
            if not piece == "" :
                cleanpieces.append(piece)
        pieces = cleanpieces

        if len(pieces) < 3 : #this means that it is a placement test instead of a course
            presubject = "None"
            precourse = "None"
            other = "Placement Test"
            concurrent = "False"
            mingrade = "None"
        else :
            precoursesubject = pieces[0].split(":")[1] #format is CourseorTest:CS330 so split on : and take second half to get CS330
            for i in range(len(precoursesubject)) :
                if precoursesubject[i].isdigit() :
                    presubject = precoursesubject[0:i]
                    precourse = precoursesubject[i:]
                    break
            mingrade = pieces[1][pieces[1].find("f")+1:]
            if "not" in pieces[2] :
                concurrent = "False"
            else :
                concurrent = "True"
        prereq = {  "Subject": subject,
                    "Course": coursenum,
                    "Pre-Subject": presubject,
                    "Pre-Course": precourse	,
                    "Other": other,
                    "Concurrent": concurrent,
                    "MinGrade": mingrade,
                    "Index": index
                }
        req_list.append(prereq)
    except :
        print("Error on " + subject + coursenum)


def parse(req, subject, coursenum) : 
    global index
    if isinstance(req, list) or isinstance(req, tuple) :
        for indreq in req :
            if indreq != "and" :
                parsereq(indreq, subject, coursenum)
        index = index + 1
    else :
        parsereq(req, subject, coursenum)
        index = index + 1
        

        
 
def splitreqs(reqs, subject, courseNum) : #split the reqs into a list that follow [(), (), (), and, (), ()] or [[(), and, ()], [(), and, ()], (), ()] where () is a req block 
                                                                                                                                       #"," is an implicit or
                                                                                                                                       #"and" is explicit
    global index
    reqssplit = []  #list to store the split requisites
    reqs = reqs.replace(" ", "") #get rid of white space
    for x in reqs.split("(") :  #I want to parse this by the () of courses. This contains the logical syntax
        for y in x.split(")") : #^
            reqssplit.append(y) 
    reqparse = [] #now we need to parse the "and"s / "or"s into another list
    for req in reqssplit :
        if not(req == "" or req == "or") : #remove empty spaces and "or"s
            andcourse = req.split("and")  #now we need to break down the inner "or"s to see if theres an "and" inside
            if len(andcourse) == 1 :      #if there isn't, (split doesnt split it into multiple strings) 
                for course in andcourse[0].split("or\n") :  #just split the string on "or" and append each bit into the new list
                    reqparse.append(course)
            else :                        #if there was an "and", we want that inside our list as another list
                templist = []
                for i in range(len(andcourse)) : #but, it deleted our explicit "and"
                    if i % 2 == 1 :              #so every other element add an "and"
                        templist.append("and")
                    templist.append(andcourse[i]) 
                reqparse.append(templist)
    reqclean = []
    print(reqparse)
    for req in reqparse :
        if isinstance(req, list) :
            templist = []
            for innerreq in req :
                if not innerreq == "\n" :
                    templist.append(innerreq)
            if len(templist) == 1 :
                reqclean.append("and")
            else :
                reqclean.append(templist)
        elif not(req == "\n" or req == "") :
            reqclean.append(req)
    print(reqclean)
    if "and" in reqclean :
        finalreqs = []

        # using list comprehension Split list into lists by particular value (got from https://www.geeksforgeeks.org/python-split-list-into-lists-by-particular-value/)
        size = len(reqclean)
        idx_list = [idx + 1 for idx, val in
                    enumerate(reqclean) if val == "and"]
        
        res = [reqclean[i: j] for i, j in
            zip([0] + idx_list, idx_list +
                ([size] if idx_list[-1] != size else []))]

        for lst in res :
            templist = []
            for i in range (len(lst)) :
                if not lst[i] == "and" :
                    templist.append(lst[i])
            finalreqs.append(templist)

        #make combinations of each [[], [], []] (https://stackoverflow.com/questions/798854/all-combinations-of-a-list-of-lists)
        finalreqs = list(itertools.product(*finalreqs))

        print(finalreqs)

        for req in finalreqs :
            parse(req, subject, courseNum)

    else :
        print(reqclean)
        for req in reqclean :
            parse(req, subject, courseNum)

with open("../data/allCourses.JSON") as allcourses :
    classes = json.load(allcourses)
    #open chrome
    for i in range(len(classes)) :
        if (i >= 0) : #use this to limit how many it actually does
            subject = classes[i]["subject"] #get the classes we have from JSON list already created (save on search and parsing time)
            courseNum = classes[i]["coursenum"] #get course num from JSON list
            print("Course : " + subject + " " + courseNum)
            builturl = URL1 + subject + URL2 + courseNum #build the URL (if we just insert the Course subject and number in the right spot we get the page for that course)
            driver = webdriver.Chrome() #open the url we just built for the course
            driver.get(builturl)
            data = driver.find_elements(By.CLASS_NAME, "ntdefault") #the main text is in this class
            text = data[0].text #get the text out of it
            if "Corequisites" in text :     #if the course has corereqs it will say so. Just use that to determine if we even need to parse
                ind = text.find("Corequisites:")
                ind2 = text.find("\nPre")
                if ind2 == -1 :
                    ind2 = len(text) + 1
                cores = text[ind + len("Corequisites:") + 1 : ind2-1]
                cores = cores.split("\n")
                if len(cores) > 1 :
                    print("Multiple cores at " + presubject + " " + precourse)
                for core in cores :
                    subjectcourse = core.split(" ")
                    presubject = subjectcourse[0]
                    precourse = subjectcourse[1]
                    other = "Corequisites"
                    concurrent = "True"
                    mingrade = "None"
                    prereq = {  "Subject": subject,
                                "Course": courseNum,
                                "Pre-Subject": presubject,
                                "Pre-Course": precourse	,
                                "Other": other,
                                "Concurrent": concurrent,
                                "MinGrade": mingrade,
                                "Index": index
                            }
                    req_list.append(prereq)
                    index =  index + 1
                     
            if "Prerequisites" in text :    #if the course has prereqs it will say so. Just use that to determine if we even need to parse

                ind = text.find("General Requirements:") #after "general requirements:" comes the prerequisites text
                reqs = text[ind + len("General Requirements:") + 1:] #parse the reqs text based on what we just found for indexes
                print(reqs)
                splitreqs(reqs, subject, courseNum)
for req in req_list :
    print(req)
outputFileName = "../data/PreCoreReq.json"  #the name of the file the courses will go
with open(outputFileName, 'w') as json_file:  #export list to JSON file
    json_string = json.dump(req_list, json_file, indent = 4)