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
errors = []

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
        if not req.strip().replace("\n", "") == "Maynotbetakenconcurrently." : #sometimes the website scraping from has errors and does not list a course or any details
            global index                                                        #get the index
            presubject = "None" #default values
            precourse = "None"
            other = "None"
            concurrent = "False"
            mingrade = "None"
            pieces = req.split("\n") #get rid of formatting
            cleanpieces = []
            for piece in pieces :
                if not piece == "" : #sometimes it was making the req pieces "" so we need to get rid of those instances
                    cleanpieces.append(piece)
            pieces = cleanpieces #just reset pieces

            if len(pieces) < 3 : #this means that it is a placement test instead of a course
                presubject = "None"
                precourse = "None"
                other = "Placement Test"
                concurrent = "False"
                mingrade = "None"
            else :
                precoursesubject = pieces[0].split(":")[1] #format is CourseorTest:CS330 so split on : and take second half to get CS330
                for i in range(len(precoursesubject)) :    #loop through cs330
                    if precoursesubject[i].isdigit() :     #once we find a digit, we know that the rest is course num
                        presubject = precoursesubject[0:i] #break apart based on found digit
                        precourse = precoursesubject[i:]
                        break
                mingrade = pieces[1][pieces[1].find("f")+1:] #"minimumgradofC" so find f and grab the next letter (probably couldve done index -1 but dont want to mess with it)
                if "not" in pieces[2] : #if it says "maynotbetakenconcurrently" it contains not so just check for that
                    concurrent = "False"
                else :
                    concurrent = "True"
            prereq = {  "Subject": subject,  #create the json piece
                        "Course": coursenum,
                        "Pre-Subject": presubject,
                        "Pre-Course": precourse	,
                        "Other": other,
                        "Concurrent": concurrent,
                        "MinGrade": mingrade,
                        "Index": index
                    }
            req_list.append(prereq) #build the JSON
    except :
        print("Error on " + subject + coursenum) #we errored here (there was a weird error on a specific one so I just added this. it just skips it)
        errors.append(subject + " " + coursenum) #keep track to see how many errors we encounter (for debugging)

def parse(req, subject, coursenum) : 
    global index
    if isinstance(req, list) or isinstance(req, tuple) : #check if its a list of requirements (ie an "and" of courses)
        for indreq in req : #go through each req in the list/tuple
            if indreq != "and" : #ignore the ands
                parsereq(indreq, subject, coursenum) #parse the reqs
        index = index + 1 #incrememnt after the loop so the "and"s have the same index
    else :
        parsereq(req, subject, coursenum) #parse them
        index = index + 1 #change the index because it was just an or
        

        
 
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
    for req in reqparse : #just clean up some of the req
        if isinstance(req, list) :
            templist = []
            for innerreq in req : #there was an error we would get ["\n", "and", "\n"] so this sorts that out by deleting the list and just putting an and
                if not innerreq == "\n" :
                    templist.append(innerreq)
            if len(templist) == 1 :
                reqclean.append("and") 
            else :
                reqclean.append(templist)
        elif not(req == "\n" or req == "") : #just make sure its not an empty req
            reqclean.append(req)
    if "and" in reqclean : #if there is an instance where are "and"ing outside of a list (req1 and req2) instead of ((req1 and req2) or (req1 and req2))
        finalreqs = []

        # using list comprehension Split list into lists by particular value (got from https://www.geeksforgeeks.org/python-split-list-into-lists-by-particular-value/)
        #turn [req1 or req2 and req3 or req4] into [[req1 or req2] and [req3 or req4]]
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
        #we need to do this because ((req1 or req2) and (req3 or req4)) it is hard to deal with in this format so we need to apply
        #some prepositional logic and do ((req1 and req3) or (req1 and req4) or (req2 and req3) or (req3 and req4))
        finalreqs = list(itertools.product(*finalreqs))

        for req in finalreqs : #parse all of the reqs
            parse(req, subject, courseNum)

    else :
        for req in reqclean :#parse all of the reqs (could condense this with above code but don't want to mess with it)
            parse(req, subject, courseNum)

with open("../data/allCourses.JSON") as allcourses :
    classes = json.load(allcourses)
    #open chrome
    for i in range(len(classes)) :
        if (i >= 0) : #use this to limit how many it actually does
            subject = classes[i]["subject"] #get the classes we have from JSON list already created (save on search and parsing time)
            courseNum = classes[i]["coursenum"] #get course num from JSON list
            builturl = URL1 + subject + URL2 + courseNum #build the URL (if we just insert the Course subject and number in the right spot we get the page for that course)
            driver = webdriver.Chrome() #open the url we just built for the course
            driver.get(builturl)
            print("Course: " + courseNum + " " + subject)
            data = driver.find_elements(By.CLASS_NAME, "ntdefault") #the main text is in this class
            text = data[0].text #get the text out of it
            
            if "Corequisites" in text :     #if the course has corereqs it will say so. Just use that to determine if we even need to parse
                ind = text.find("Corequisites:") #this is basically the parse function but for corequisites instead of prerequisites 
                ind2 = text.find("\nPre")
                if ind2 == -1 :
                    ind2 = len(text) + 1
                cores = text[ind + len("Corequisites:") + 1 : ind2-1]
                cores = cores.split("\n")
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
                splitreqs(reqs, subject, courseNum)
#for req in req_list :
#    print(req)
outputFileName = "../data/PreCoreReq.json"  #the name of the file the courses will go
with open(outputFileName, 'w') as json_file:  #export list to JSON file
    json_string = json.dump(req_list, json_file, indent = 4)
print("Not entered into json file")
for error in errors :
    print(error)