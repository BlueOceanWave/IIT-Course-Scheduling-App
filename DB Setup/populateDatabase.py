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

# Extract json files
classes_json = open('IPRO-497-Group-D/DB Setup/data/Fall_2023.json')
courses_json = open('IPRO-497-Group-D/DB Setup/data/allCourses.json')
subjects_json = open('IPRO-497-Group-D/DB Setup/data/subjects.json')
requirements_json = open('IPRO-497-Group-D/DB Setup/data/PreCoreReq.json')
majorrequirements_json = open('IPRO-497-Group-D/DB Setup/data/majorRequirements.json')
classes = json.load(classes_json)
courses = json.load(courses_json)
subjects = json.load(subjects_json)
requirements = json.load(requirements_json)
majorrequirements = json.load(majorrequirements_json)


def extractTime(time):
    ABORT_VALUE = None

    #Separate time and am/pm
    parts = time.split()
    if len(parts) != 2:
        return ABORT_VALUE

    # Separate minute form hour
    time_split = parts[0].split(':')
    if len(time_split) != 2:
        return ABORT_VALUE

    # Check that time is a number
    hour, min = time_split
    try:
        int(hour)
        int(min)
    except:
        return ABORT_VALUE

    # Check am/pm is valid
    period = parts[1].lower()
    if period not in ['am', 'pm']:
        return ABORT_VALUE
    
    # # Convert to military time
    # if period == 'pm':
    #     hour = int(hour) + 12

    # Return the time
    return f'{hour}:{min} {period.upper()}'

def extractDate(date):
    ABORT_VALUE = None

    # Check that date has 3 parts
    parts = date.split()
    if len(parts) != 3:
        return ABORT_VALUE
    month, day, year = parts

    # Check the month is valid:
    month = month.lower()
    months = 'jan feb mar apr may jun jul aug sep oct nov dec'.split()
    if month not in months:
        return ABORT_VALUE
    
    # Pad to 2 digits
    month = str(months.index(month)).zfill(2)

    # Check the day and year are valid
    day = day[:-1] #removes the comma
    try:
        int(day)
        int(year)
    except:
        return ABORT_VALUE
    
    # Return as YYYY-MM-DD
    return f'{year}-{month}-{day}'

def extractDays(days):
    # Make sure all days are valid
    for day in days:
        if day not in 'MTWRF':
            return None
    
    return days

def extractOneOf(element, list):
    if element not in list:
        return None
    
    return element

def extractClassData(entry):
    # 'title', 'CRN', 'sID', 'cID', 'sNum', 'term', 'campus', 'online', 'startTime', 'endTime', 
    # 'days', 'building', 'room', 'startDate', 'endDate', 'cType', 'instructors'
    
    # Check data entries are appropriate
    # Convert entries if necessary
    result = {
        'title': entry['title'],
        'CRN': entry['CRN'],
        'sID': entry['sID'],
        'cID': entry['cID'],
        'sNum': entry['sNum'],
        'term': entry['term'],
        'campus': entry['campus'],
        'online': extractOneOf(entry['online'], ['Online', 'Traditional', 'Non Traditional']),
        'startTime': extractTime(entry['startTime']),
        'endTime': extractTime(entry['endTime']),
        'days': extractDays(entry['days']),
        'building': entry['building'],
        'room': entry['room'],
        'startDate': entry['startDate'],
        'endDate': entry['endDate'],
        'cType': entry['cType'],
        'instructors': entry['instructors']
    }

    return result

def extractRequirementData(entry):
    result = {
        "sID": entry['Subject'],
        "cID": entry['Course'],
        "rsID": entry['Pre-Subject'],
        "rcID": entry['Pre-Course'],
        "concurrent": '1' if entry['Concurrent'] == 'True' else '0',
        "minGrade": extractOneOf(entry['MinGrade'], ['A', 'B', 'C', 'D', 'S', 'P']),
        "index": entry['Index']
    }

    return result



def createDatabase():
    cursor = connection.cursor()

    with open('IPRO-497-Group-D/DB Setup/SchedulingAppDatabase.sql', 'r') as sql_file:
        sql_commands = sql_file.read()
        cursor.execute(sql_commands)
    
    connection.commit()
    cursor.close()

def addSubjectsToDatabse(subjects):

    cursor = connection.cursor()

    for subject in subjects:
        subjectQuery = 'INSERT INTO subjects (sID, lID) VALUES (%s, %s)'
        subjectValues = (subject['sID'], subject['lID'])

        cursor.execute(subjectQuery, subjectValues)
    
    connection.commit()
    cursor.close()

    print("Added subjects to databse")

def addCoursesToDatabse(courses):
    
    cursor = connection.cursor()

    for course in courses:
        courseQuery = 'INSERT INTO courses (sID, cID, title, hours, description) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (sID, cID) DO NOTHING'
        courseValues = tuple(course[i] for i in ['subject', 'coursenum', 'title', 'hours', 'desc'])

        cursor.execute(courseQuery, courseValues)

    connection.commit()
    cursor.close()

    print('Added courses to database')

def addClassesToDatabase(classes):

    cursor = connection.cursor()
    
    for course in classes:
    
        course_data = extractClassData(course)
    
        # Create queries
        classQuery = 'INSERT INTO classes (CRN, sID, cID, sNUM, term, days, startTime, endTime, campus, online, building, room) \
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        classValues = tuple(course_data[i] for i in ['CRN', 'sID', 'cID', 'sNum', 'term', 'days', 'startTime', 'endTime', 'campus', 'online', 'building', 'room'])

        termQuery = "INSERT INTO term (term, startDate, endDate) VALUES (%s, %s, %s) ON CONFLICT (term) DO NOTHING"
        termValues = tuple(course_data[i] for i in ['term', 'startDate', 'endDate'])
        
        # Execute queries. Order is important to ensure foreign keys have references
        # Add Term
        try:
            cursor.execute(termQuery, termValues)
        except:
            print(f"Couldn't add term for {course_data['sID']} {course_data['cID']}")

        # Add class
        try:
            cursor.execute(classQuery, classValues)
        except:
            print(f"Couldn't add class {course_data['sID']} {course_data['cID']}")

        # Add instructors
        try:
            # Execute query for each instructor
            for instructor in course_data['instructors']:
                instructorQuery = "INSERT INTO instructors (CRN, instructor) VALUES (%s, %s)"
                instructorValues = (course_data['CRN'], instructor)
                cursor.execute(instructorQuery, instructorValues)
        except:
            print(f"Couldn't add instructors for {course_data['sID']} {course_data['cID']}\n")

        connection.commit()
    
    cursor.close()

    print(f'Added classes, instructors, and terms to Database')

def addRequirementsToDatabase(requirements):
    cursor = connection.cursor()

    for requirement in requirements:
        requirement_data = extractRequirementData(requirement)

        # Make sure that the class has requirements, and that its not a range
        if requirement_data['rsID'] != 'None' and requirement_data['rcID'] != 'None' and ('to' not in requirement_data['rcID']):
          if not (requirement_data['rsID'] == 'HUM' and requirement_data['rcID'] in ['102', '104', '106']):
            requirementQuery = 'INSERT INTO requirements (sID, cID, rsID, rcID, concurrent, minGrade, index) VALUES (%s, %s, %s, %s, %s, %s, %s)'
            requirementValues = tuple(requirement_data[i] for i in ['sID', 'cID', 'rsID', 'rcID', 'concurrent', 'minGrade', 'index'])

            try:
                cursor.execute(requirementQuery, requirementValues)
            except:
                print(f"Couldn't add requirement {requirement_data['rsID']} {requirement_data['rcID']} for {requirement_data['sID']} {requirement_data['cID']}")

            connection.commit()

        # If the requirements is a range, add each class separately    
        elif 'to' in requirement_data['rcID']:
            # Get beginning and end of range
            low, high = requirement_data['rcID'].split('to') 

            # Get all valid cIDs given the sID
            cursor.execute('SELECT cID FROM courses WHERE sID = %s', (requirement_data['rsID'],))
            getValidcIDs = cursor.fetchall()

            # Add each cID in the range as a coreq
            i = 1
            for (cID,) in getValidcIDs:
                if int(cID) in range(int(low), int(high)): # Check to see if the cID is in the range
                    requirementQuery = 'INSERT INTO requirements (sID, cID, rsID, rcID, concurrent, minGrade, index) VALUES (%s, %s, %s, %s, %s, %s, %s)'
                    requirementValues = [requirement_data[i] for i in ['sID', 'cID', 'rsID', 'rcID', 'concurrent', 'minGrade', 'index']]
                    requirementValues[3] = cID # Update cID
                    requirementValues[-1] = int(requirementValues[-1])*1000 + i # Update index to make them 'or' requirements
                    requirementValues = tuple(requirementValues)

                    try:
                        cursor.execute(requirementQuery, requirementValues)
                    except:
                        print(f"Couldn't add requirement {requirement_data['rsID']} {requirement_data['rcID']} for {requirement_data['sID']} {requirement_data['cID']} from range {low} to {high}")

                    connection.commit()

                    i += 1 # Update index value to make them unique
        

    cursor.close()

    print('Added requirements to database')

def addMajorRequirementsToDatabase() :

    #list of things to be added manually :
        #Computer Science
            #CS electives
            #Science Electives
            #Free Electives
        
        #Computer and Cybersecurity Engineering
            #Cybersecurity Software engineering elective
            #Career Elective '', I

        #Computer Engineering
            #Professional ECE electives
            #Career Elective '', I, II, III

    majors = []
    start = 1
    index = 8

    cursor = connection.cursor()
    majorQuery = 'INSERT INTO majors (major, requirement, sID, cID, hours, index) VALUES (%s, %s, %s, %s, %s, %s)'

    for major in majorrequirements : #get all majors in majorrequirements
        try:  #need to manually add core requirements (IPRO and hum/social sciences)
            #cursor.execute(majorQuery, [major, 'IPRO Requirement', "IPRO I", "497", '6', '1']) 
            #cursor.execute(majorQuery, [major, 'IPRO Requirement', "IPRO II", "497", '6', '2'])
            for (i, cid) in [(1, '200'), (2, '202'), (3, '204'), (4, '206'), (5, '208')] :
                cursor.execute(majorQuery, [major, 'Humanities Requirement', "HUM", cid, '3', str(2 + i)])

                #-------------------I need to add higher level humanity requirements here ------------------------
                #-------------------I need to add higher level humanity requirements here ------------------------
                #-------------------I need to add higher level humanity requirements here ------------------------
                
        except Exception as error:
            print(f"Couldn't add IPRO and Humanities for {major}")
            print(error)

        for requirement in majorrequirements[major] : #get all the individual requirements
            if 'IPRO' in requirement : #if its an ipro, dont process it
                pass
            elif (start == 1) and ('(' in requirement) and (')' in requirement) : #if it is the first line in requirements and can be processed (may not need start)
                hours = requirement[requirement.index('(') + 1 : requirement.index(')')] #find the values between (hours)
                if '-' in hours : #if it is something like 2-3 hours
                    hours = str(min(list(map(lambda x : int(x), hours.split('-'))))) #get both values from string, make them ints, min them, and then convert back to string
                start += 1 #make it so this doesnt keep running

            for classes in  majorrequirements[major][requirement]: #the json is a dictionary of majors, which the keys are a dictionary of requirement sections

                if not ('Select' in classes or 'Choose' in classes or 'See' in classes or '(' in classes or 'Elective' in classes) : #everytime I encountered an invalid entry I added a case to ignore it
                    
                    for classes in classes.split(' or ') : #if the values had class or class, we want them to have the same index
                        subcourse = classes.split(' ')     #split the class from "sid cid"
                        sID = subcourse[0]
                        cID = subcourse[1]
                        try: #try to add to database
                            cursor.execute(majorQuery, [major, requirement, sID, cID, hours, str(index)]) #insert all the values
                            connection.commit() #commit to the database
                        except Exception as error : #if error, tell us on what value and why
                            print(f"Could not add {major} requirement {requirement} with course {sID} {cID}")
                            print(error)
                    index += 1 #increment index so that new values are not put together
            start = 1



# Deletes all tables and recreates them
createDatabase() 

# Add table entries in order to ensure foriegn keys are satisfied
addSubjectsToDatabse(subjects) 
addCoursesToDatabse(courses)
addClassesToDatabase(classes)
addRequirementsToDatabase(requirements)
addMajorRequirementsToDatabase()