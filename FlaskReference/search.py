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

cs116 = Section()
cs116.course.hasLabSection()
cs116.course.hasRecitationSection()

class Section:
        def __init__(self, crn, snum, days, starttime, endtime, campus, online, building, room, instructor, course=None, enrollment=None, enrollmentmax=None, waitlist=None):
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
            self.instructors = [instructor]

            self.course = course

        def linkCourse(self, course):
            self.course = course

        def addInstructor(self, instructor):
            self.instructors.append(instructor)

        def isLab(self):
            return self._getSectionType() == 'Lab'
        
        def isRecitation(self):
            return self._getSectionType() == 'Recitation'
        
        def daysToIndex(self):
            # Convert day (M-F) to index (1-5)
            result = []
            for day in self.days:
                result.append('MTWRF'.index(day)+1)

            return result

        def _toStandardTime(self, militaryTime):
            hr, min, sec = militaryTime.split(':')
            suffix = 'AM' if int(hr)<12 else 'PM'
            
            # Convert 24 hour time to 12 hour time
            if int(hr) == 0 or int(hr) == 12:
                hr = '12'
            elif int(hr)>12:
                hr = str(int(hr)-12)

            return f'{hr}:{min} {suffix}'

        def _toAbsoluteTime(self, militaryTime):
            hr, min, sec = militaryTime.split(':')

            # Returns time of 17:50 to 1750 as a number for camprison purposes
            return int(hr)*100+int(min)

        def _getAbsoluteTimeRange(self):
            return (self._toAbsoluteTime(self.starttime), self._toAbsoluteTime(self.endtime))

        def _getSectionType(self):
            if 'L' in self.snum:
                return 'Lab'
            elif 'R' in self.snum:
                return 'Recitation'
            else:
                return 'Lecture'

        def __str__(self):
            result = f'{self.crn} - '
            result += f'{self.enrollment} seats avail. '
            result += f'| {self._getSectionType()} ({self.online}) '
            result += f'~ {", ".join(self.instructors)} '
            if self.days != 'None':
                result += f'~ {self.days} from {self._toStandardTime(self.starttime)} to {self._toStandardTime(self.endtime)} '
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
        # Link the section to this course
        section.linkCourse(self)

        # Add if its a new section
        if section not in self.sections:
            self.sections.append(section)
        # Otherwise update the existing section with the new instructor
        else:
            existing_section = self.sections[self.sections.index(section)]
            existing_section.addInstructor(section.instructors[0])

    def hasLabSection(self):
        # Check to see if any sections are a Lab
        for section in self.sections:
            if 'L' in section.snum:
                return True
            
        return False
    
    def hasRecitationSection(self):
        # Check to see if any sections are a Lab
        for section in self.sections:
            if 'R' in section.snum:
                return True
            
        return False
  
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
    'getActiveClasses' : 'SELECT * FROM classes INNER JOIN courses USING (sID, cID) INNER JOIN subjects USING (sID) INNER JOIN instructors USING (crn)',
}

cursor = connection.cursor()

cursor.execute(query['getActiveClasses'])
classes = cursor.fetchall()

cursor.execute(query['getSubjects'])
subjects = [subject for (subject,) in  cursor.fetchall()]

cursor.close()

# Attribute indexes:
#  0    1    2     3     4    5        6         7       8       9        10      11     12    13        14        15     16
# sid, cid, crn, snum, term, days, starttime, endtime, campus, online, building, room, title, hours, description, lid, instructor
attr_idx = {
    'crn': 0,
    'sid': 1,
    'cid': 2,
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
    'instructor': 16
}


# Get attributes for searching
def getSearchAttributes(attributes):
    cols = ['sid', 'cid', 'title', 'crn']
    return [str(attributes[attr_idx[i]]) for i in cols]

# Get attributes for class object
def getCourseAttributes(attributes):
    cols = ['sid', 'cid', 'title', 'description', 'hours', 'term']
    return [str(attributes[attr_idx[i]]) for i in cols]

# Get attributes for section object
def getSectionAttributes(attributes):
    #crn, snum, days, starttime, endtime, campus, online, building, room, instructor, enrollment, enrollmentmax, waitlist
    cols = ['crn', 'snum', 'days', 'starttime', 'endtime', 'campus', 'online', 'building', 'room', 'instructor']
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

    crn = None
    if len(search_terms) == 1 and search_terms[0].isnumeric() and len(search_terms[0]) == 5:
        crn = search_terms[0]

    # Search all classes for a match
    matches = []

    for raw_class in classes:
        search_attributes = getSearchAttributes(raw_class)
        
        # If we're searching for crn's, then ignore all other attributes
        if crn is not None:
            if crn == search_attributes[3]:
                matches.append(raw_class)
                continue

        # If the subject ID was specified, match it. If not, continue
        elif sID is None or sID.lower() == search_attributes[0].lower():
            # Check if any other search terms are left
            # If not, return any class of that subject
            if len(search_terms) == 0:
                matches.append(raw_class)
                continue

            # If we get here, then other terms are left for us to match
            allTermsPresent = True
            for term in search_terms:
                if term.lower() not in ' '.join(search_attributes[:-1]).lower():
                    allTermsPresent = False
            
            # Only add if all the terms are present
            if allTermsPresent:            
                matches.append(raw_class)

    # Convert the results into Course and Section objects    
    courses = []    
    for match in matches:
        course = Course(*getCourseAttributes(match))
        section = Section(*getSectionAttributes(match))

        # If its a new course, add it
        if course not in courses:
            course.addSection(section)
            courses.append(course)
        # Otherwise update the existing course
        else:
            course = courses[courses.index(course)]
            course.addSection(section)
    
    return courses

# for course in search('cs 100'):
#     print(course)
#     for section in course.sections:
#         print(f'\t{section}')
#     print()


def show_search_results(searchbar):    
    output = ""
    for course in search(searchbar):
        output = output + str(course)
        for section in course.sections:
            output = output + f'\t{str(section)}'+ '\n' + ""
        output = output + '\n' + ""
    return output

# print(show_search_results("ece 443"))

# for c in search('cs 330'):
#     print(c)
#     for s in c.sections:
#         print("  ", s)
#     print()