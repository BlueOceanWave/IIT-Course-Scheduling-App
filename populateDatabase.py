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

classes_json = open('Fall_2023.json')
classes = json.load(classes_json)

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
    
    return days[:5]

def extractOneOf(element, list):
    if element not in list:
        return None
    
    return element[:10]



def extractClassData(entry):
    # 'title', 'CRN', 'sID', 'cID', 'sNum', 'term', 'campus', 'online', 'startTime', 'endTime', 
    # 'days', 'building', 'room', 'startDate', 'endDate', 'cType', 'instructors'
    
    # Check data entries are appropriate
    # Convert entries if necessary
    result = {
        'title': entry['title'],
        'CRN': entry['CRN'],
        'sID': entry['sID'][:10],
        'cID': entry['cID'],
        'sNum': entry['sNum'][:10],
        'term': entry['term'],
        'campus': extractOneOf(entry['campus'], ['Internet','Mies','Internship','Lecture','International','Downtown']),
        'online': extractOneOf(entry['online'], ['Online', 'Traditional', 'Non Traditional']),
        'startTime': extractTime(entry['startTime']),
        'endTime': extractTime(entry['endTime']),
        'days': extractDays(entry['days']),
        'building': entry['building'][:30],
        'room': entry['room'][:10],
        'startDate': entry['startDate'],
        'endDate': entry['endDate'],
        'cType': entry['cType'],
        'instructors': entry['instructors'][0][:30]
    }

    return result

def addClassesToDatabase(classes, major):

    cursor = connection.cursor()
    
    for course in classes:
        if course['sID'].lower() == major.lower():
            course_data = extractClassData(course)

            classQuery = 'INSERT INTO classes (CRN, sID, cID, sNUM, term, days, startTime, endTime, campus, online, instructor, building, room) \
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            classValues = tuple(course_data[i] for i in ['CRN', 'sID', 'cID', 'sNum', 'term', 'days', 'startTime', 'endTime', 'campus', 'online', 'instructors', 'building', 'room'])

            # termQuery = "INSERT INTO term (term, startDate, endDate) VALUES (%s, %s, %s)"
            # termValues = tuple(course_data[i] for i in ['term', 'startDate', 'endDate'])
            # cursor.execute(termQuery, termValues)
            
            
            cursor.execute(classQuery, classValues)

            # try:
            #     cursor.execute(classQuery, classValues)
            # except Exception as e:
            #     print(e)
            #     print(course_data['sID'], course_data['cID'], course_data['CRN'])
            #     print(*map(lambda x: 0 if x==None else len(x), classValues))

    connection.commit()
    cursor.close()

    print(f'Added {major} classes to Database')


addClassesToDatabase(classes, 'CS')








# print("classes: ", len(classes))
# # print("keys: ", classes[0].keys())

# print(extractDate("DEC 09. 2023"))

# camp = set()
# online = set()
# term = set()
# room = set()

# for c in classes[:]:
#     camp.add(c['campus'])
#     online.add(c['online'])
#     term.add(c['term'])
#     room.add(c['room'])

# print(camp)
# print(online)
# print(term)
# print([len(b) for b in room if len(b) > 10])




# def insertClass():
#     return

# def insertTerm():
#     return

