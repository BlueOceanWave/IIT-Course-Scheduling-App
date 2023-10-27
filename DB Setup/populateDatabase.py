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
classes_json = open('DB Setup/data/Fall_2023.json')
courses_json = open('DB Setup/data/allCourses.json')
subjects_json = open('DB Setup/data/subjects.json')
requirements_json = open('DB Setup/data/PreCoreReq.json')
classes = json.load(classes_json)
courses = json.load(courses_json)
subjects = json.load(subjects_json)
requirements = json.load(requirements_json)


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

    with open('DB Setup/SchedulingAppDatabase.sql', 'r') as sql_file:
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

# Deletes all tables and recreates them
createDatabase() 

# Add table entries in order to ensure foriegn keys are satisfied
addSubjectsToDatabse(subjects) 
addCoursesToDatabse(courses)
addClassesToDatabase(classes)
addRequirementsToDatabase(requirements)