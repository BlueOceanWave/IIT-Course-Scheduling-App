#import schedule.py
import psycopg2
import json

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

'''class Recommender(self, major, majorRequirements, remainingReqs, taken) :
    def __init__(self, user) :
        self.major = getMajor(user)
        self.majorRequirements = getReqs(major)
        self.taken = getTaken(user)'''
        

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
        return taken
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
    modreqs = reqs
    uniquereqs = list(set([(i[1], i[4]) for i in reqs])) #get unique set of requirements
    genreqs = {} #dictionary of credit hours
    classesgenreqs = {} #dictionary of available classes
    for req in uniquereqs : #go through recs and make a dictionary of req name and credit hours needed
        genreqs[req[0]] = req[1]

    print(reqs)
    for req in reqs : #make a dictionary of classes that fulfill a requirement
        print(req)
        reqname = req[1] 
        if reqname in classesgenreqs : #for some reason need to do this in multiple steps, it returns none if done in one
            cs = (str(req[2]) + str(req[3])) #this is something like 'CS480'

            classes = classesgenreqs[reqname] #get the list of requirements already in it
            classes.append(cs) #add new one
            
            classesgenreqs[reqname] = classes #reset the dictionary key value pair
        else :
            classesgenreqs[reqname] = [str(req[2]) + str(req[3])] #initialize the pair

    taken = [str(i[0]) + str(i[1]) for i in taken] #remove the tuple aspect from classes

    for requirement in reqs : #here is where I want to remove the requirements I have already taken
        req = str(requirement[2]) + str(requirement[3]) #build the requirement to match taken
        if req in taken : #see if taken
            taken.remove(req) #remove it from taken so that it doesnt double count it for multiple sections
            classes = classesgenreqs[requirement[1]]
            classes.remove(str(requirement[2]) + str(requirement[3]))
            classesgenreqs[requirement[1]] = classes #remove the class from requirements, this way we know what options are still available.
        

def recommendClasses(reqs, major) :
    pass

def recommendCourses(user) :
    major = getMajor(user) #get what major they are from data base
    taken = getTaken(user) #get what classes they've taken from the database
    reqs = getReqs(major)  #get their requirements into a list
    reqs = removeReqs(reqs, taken) #remove requirements that are completed. from this list of reqs we can determine what classes to recommend
    return recommendClasses(reqs, major) #recommend the classes

recommendCourses('hansgutts')