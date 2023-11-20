#import schedule.py
import psycopg2
import json
import random
import schedule
import search

# Connect to PostgreSQL database
connection = psycopg2.connect(
    dbname='NewDB',
    user='postgres',
    password='123456',
    host='localhost',
    port='5432'
)

class InvalidMajor(Exception) :
    "Major is invalid"
    pass

cursor = connection.cursor()

def getMajor(user) :
    try :  #retrieve major from db
        cursor = connection.cursor() 
        majorQuery = "SELECT major FROM accounts WHERE username=%s"
        cursor.execute(majorQuery, [user])
        major = cursor.fetchall()
        major = major[0][0]
        if major == 'Computer Science' : #get official name of major
            return "Bachelor of Science in Computer Science"
        elif major == "Computer Engineering" :
            return "Bachelor of Science in Computer and Cybersecurity Engineering"
        elif major == "Computer and Cybersecurity Engineering" : 
            return "Bachelor of Science in Computer Engineering"
        else : 
            raise InvalidMajor #if there is no major (some weird error), raise an exception so that we know where things went wrong
    except Exception as e :
        print("Error recommending in getMajor: " + str(e))

def getTaken(user) :
    try :   #get taken courses
        cursor = connection.cursor()
        majorQuery = "SELECT sid, cid FROM taken WHERE username=%s"
        cursor.execute(majorQuery, [user])
        taken = cursor.fetchall()
        takenfinal = []
        for took in taken :
            hourQuery = "SELECT sid, cid, hours FROM courses WHERE sid=%s and cid=%s"
            cursor.execute(hourQuery, [took[0], took[1]])
            andHours = cursor.fetchall()
            takenfinal.append(andHours[0])
        return takenfinal
    except Exception as e :
        print("Error recommending: " + str(e))

def getReqs(major) :
    try : #get the requirements of the major 
        cursor = connection.cursor()
        majorQuery = "SELECT * FROM majors WHERE major=%s"
        cursor.execute(majorQuery, [major])
        reqs = cursor.fetchall()
        return reqs
    except Exception as e :
        print("Error recommending: " + str(e))

def removeReqs(reqs, taken) : #here is where I will remove satisfied requirements. shouldnt recommend a math course if all math reqs are filled

    uniquereqs = list(set([(i[1], i[4]) for i in reqs])) #get unique set of requirements
    genreqs = {} #dictionary of credit hours
    classesgenreqs = {} #dictionary of available classes
    for req in uniquereqs : #go through recs and make a dictionary of req name and credit hours needed
        genreqs[req[0]] = req[1]

    for req in reqs : #make a dictionary of classes that fulfill a requirement
        reqname = req[1] 
        if reqname in classesgenreqs : #for some reason need to do this in multiple steps, it returns none if done in one
            cs = (str(req[2]) + str(req[3])) #this is something like 'CS480'

            classes = classesgenreqs[reqname] #get the list of requirements already in it
            classes.append(cs) #add new one
            
            classesgenreqs[reqname] = classes #reset the dictionary key value pair
        else :
            classesgenreqs[reqname] = [str(req[2]) + str(req[3])] #initialize the pair
    takenhours = {(str(i[0]) + str(i[1])): i[2] for i in taken}
    taken = [str(i[0]) + str(i[1]) for i in taken] #remove the tuple aspect from classes

    for requirement in reqs : #here is where I want to remove the requirements I have already taken

        req = str(requirement[2]) + str(requirement[3]) #build the requirement to match taken

        if req in taken : #see if taken

            if requirement[1] in classesgenreqs : #need to make sure the requirement hasn't been removed, and that social sciences came from two fields
                

                taken.remove(req) #remove it from taken so that it doesnt double count it for multiple sections
                classes = classesgenreqs[requirement[1]]
                classes.remove(str(requirement[2]) + str(requirement[3]))
                classesgenreqs[requirement[1]] = classes #remove the class from requirements, this way we know what options are still available.
                genreqs[requirement[1]] = genreqs[requirement[1]] - int(takenhours[req])

                if genreqs[requirement[1]] <= 0 :
                    del genreqs[requirement[1]]
                    del classesgenreqs[requirement[1]]

    if 'Free Elective' in uniquereqs : #since there are some free elective sections in some majors (dont have this in database because I dont know how to represent it)
        for take in taken :
            taken.remove(take)
            genreqs['Free Elective'] = genreqs['Free Elective'] - int(requirement[4])
            if genreqs['Free Elective'] <= 0 :
                del genreqs['Free Elective']
                del classesgenreqs['Free Elective']

    # print("classesgenreqs: ", classesgenreqs) #this is a dictionary of requirements and classes to fill that requirement
    # print("genreqs: ", genreqs)        #this is a dictionary of requirements and credit hours to fill that requirement
    # print("taken: ", taken)          #this is the list of classes taken
    
    return (classesgenreqs, genreqs)  #this returns two dictionaries. Both have the same keys but one returns credit hours still needed to fulfill this requirement 
                                                                                            #the other returns courses that will satisfy that requirement


def getsidcid(course) :
    return (course[0:len(course)-3], course[len(course)-3:])

def recommendClasses(classesreqs, hoursreqs, taken) : #decide which classes to recommend and return [(crn, cs100), ...]
    cursor = connection.cursor() #set up objects
    sched = schedule.Schedule()

    classesQuery = "SELECT * FROM classes WHERE sid=%s AND cid=%s" #set up queries
    instructorQuery = "SELECT * FROM instructors WHERE crn = %s"
    hoursQuery = "SELECT hours FROM courses WHERE sid=%s and cid=%s"

    recs = [] #the list of recommendations to return
    tothours = 0 #the number of credit hours
    sorted_hoursreqs = sorted(hoursreqs.items(), key=lambda x:x[1], reverse=True) #get a sorted list of requirements by credit hours

    for (req, hours) in sorted_hoursreqs : #loop through the sorted list
        sections = []

        possible = classesreqs[req]
        recommend = possible[0]

        possible = possible[1:]

        cursor.execute(classesQuery, getsidcid(recommend))
        sections = cursor.fetchall()

        for (crn, sid, cid, snum, semester, days, starttime, endtime, campus, online, building, room) in sections :

            cursor.execute(hoursQuery, (sid, cid))
            coursehours = cursor.fetchall()[0][0]

            if tothours + coursehours <= 18 and coursehours > 0 and req != 'Free Elective':

                cursor.execute(instructorQuery, [crn])
                instructor = cursor.fetchall()[0][1]

                if days is None :
                    days = 'None'

                section = search.Section(crn, snum, days, str(starttime), str(endtime), campus, online, building, room, instructor)
                
                

                sched.addSection(section)

                if len(sched.detectTimeConflict()) == 0 :
                    tothours += coursehours
                    recs.append((crn, recommend, coursehours))
                    break
                else :
                    sched.removeSection(section)
    for section in sched.sections :
        sched.removeSection(section)
    cursor.close()
    return recs

def remainingCourses(user):
    major = getMajor(user) #get what major they are from data base
    taken = getTaken(user) #get what classes they've taken from the database
    reqs = getReqs(major)  #get their requirements into a list
    (classesreqs, hoursreq) = removeReqs(reqs, taken)
    return classesreqs

def remainingHours(user):
    major = getMajor(user) #get what major they are from data base
    taken = getTaken(user) #get what classes they've taken from the database
    reqs = getReqs(major)  #get their requirements into a list
    (classesreqs, hoursreq) = removeReqs(reqs, taken)
    return hoursreq

def recommendCourses(user) :
    major = getMajor(user) #get what major they are from data base
    taken = getTaken(user) #get what classes they've taken from the database
    reqs = getReqs(major)  #get their requirements into a list
    (classesreqs, hoursreq) = removeReqs(reqs, taken) #remove requirements that are completed. from this list of reqs we can determine what classes to recommend
    return recommendClasses(classesreqs, hoursreq, taken) #recommend the classes

# remainingCourses('mom')
# remainingHours('mom')
#print(recommendCourses('mom'))