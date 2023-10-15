import psycopg2
import json
import time
import re

# Connect to PostgreSQL database
connection = psycopg2.connect(
    dbname='NewDB',
    user='postgres',
    password='123456',
    host='localhost',
    port='5432'
)

class Section:
        def __init__(self, crn, snum, days, starttime, endtime, campus, online, building, room, enrollment=None, enrollmentmax=None, waitlist=None):
            self.crn = crn
            self.snum = snum
            self.days = days
            self.starttime = starttime
            self.endtime = endtime
            self.campus = campus
            self.online = online
            self.building = building
            self.room = room
            self.enrollment = enrollment
            self.enrollmentmax = enrollmentmax
            self.waitlist = waitlist

        def __str__(self):
            result = ''
            result += f'{self.enrollment} seats avail. '
            result += f'| {"Lab" if self.snum[0]=="L" else "Lecture"} ({self.online}) '
            #result += f'~ {",".join(self.instructors)} '
            if self.days != None:
                result += f'~ {self.days} from {self.starttime} to {self.endtime} '
                if self.building != 'TBA':
                    result += f'in {self.building} {self.room}'
            

            return result

        def __eq__(self, section):
            return self.crn == section.crn
class Course:
    
    def __init__(self, sid, cid, title, description, hours, term):
        self.sid = sid
        self.cid = cid
        self.title = title
        self.term = term
        self.hours = hours
        self.description = description
        self.sections = []
    
    def addSection(self, section):
        self.sections.append(section)

    def __str__(self):
        result = ''
        result += f'{self.sid} {self.cid}: {self.title}'
        result += f'\n{self.description}'

        return result

    def __eq__(self, course):
        isEqual = self.sid.lower() == course.sid.lower() and self.cid.lower() == course.cid.lower() 
        return isEqual
    
query = {
    'getSubjects': 'SELECT DISTINCT sID AS subject FROM subjects;',
    'getActiveClasses' : 'SELECT * FROM classes INNER JOIN courses USING (sID, cID) INNER JOIN subjects USING (sID) ',
}

cursor = connection.cursor()

cursor.execute(query['getActiveClasses'])
classes = cursor.fetchall()

cursor.execute(query['getSubjects'])
subjects = [subject for (subject,) in  cursor.fetchall()]

cursor.close()

# Attribute indexes:
#  0    1    2     3     4    5        6         7       8       9        10      11     12    13        14        15
# sid, cid, crn, snum, term, days, starttime, endtime, campus, online, building, room, title, hours, description, lid
attr_idx = {
    'sid': 0,
    'cid': 1,
    'crn': 2,
    'snum': 3,
    'term': 4,
    'days': 5,
    'starttime': 6,
    'endtime': 7,
    'campus': 8,
    'online': 9,
    'building': 10,
    'room': 11,
    'title': 12,
    'hours': 13,
    'description': 14,
    'lid': 15,
}


# Get attributes for searching
def getSearchAttributes(attributes):
    cols = ['sid', 'cid', 'title']
    return [str(attributes[attr_idx[i]]) for i in cols]

# Get attributes for class object
def getCourseAttributes(attributes):
    cols = ['sid', 'cid', 'title', 'description', 'hours', 'term']
    return [str(attributes[attr_idx[i]]) for i in cols]

# Get attributes for section object
def getSectionAttributes(attributes):
    #crn, snum, days, starttime, endtime, campus, online, building, room, enrollment, enrollmentmax, waitlist
    cols = ['crn', 'snum', 'days', 'starttime', 'endtime', 'campus', 'online', 'building', 'room']
    return [str(attributes[attr_idx[i]]) for i in cols]

# Searches classes
def search(searchbar):
    # Split input into individual tokens
    search_terms = searchbar.split()

    # Check to see if any term is a subject ID
    sID = None
    for term in search_terms:
        if term.lower() in ' '.join(subjects).lower():
            sID = term
            search_terms.remove(term)
            break

    # Search all classes for a match
    matches = []
    for c in classes:
        search_attributes = getSearchAttributes(c)
        
        # If the subject ID was specified, match it. If not, continue
        if  sID is None or sID.lower() == search_attributes[0].lower():
            # Check if any other search terms are left
            # If not, return any class of that subject
            if len(search_terms) == 0:
                matches.append(c)
                continue

            # If we get here, then other terms are left for us to match
            allTermsPresent = True
            for term in search_terms:
                if term.lower() not in ' '.join(search_attributes).lower():
                    allTermsPresent = False
            
            # Only add if all the terms are present
            if allTermsPresent:            
                matches.append(c)

    # Convert the results into Course and Section objects    
    courses = []    
    for match in matches:
        course = Course(*getCourseAttributes(match))
        section = Section(*getSectionAttributes(match))

        if course not in courses:
            course.addSection(section)
            courses.append(course)
        else:
            course = courses[courses.index(course)]
            course.addSection(section)

    return courses

for course in search('cs algorithms'):
    print(course)
    for section in course.sections:
        print(f'\t{section}')
    print()
