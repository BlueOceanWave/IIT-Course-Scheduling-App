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
    #Separate time and am/pm
    parts = time.split()
    if (len(parts) != 2):
        return None

    # Separate minute form hour
    time_split = parts[0].split(':')
    if (len(time_split) != 2):
        return None

    # Check that time is a number
    hour, min = time_split
    try:
        int(hour)
        int(min)
    except:
        return None

    # Check am/pm is valid
    period = parts[1].lower()
    if (period not in ['am', 'pm']):
        return None
    
    # Convert to military time
    if (period == 'pm'):
        hour = int(hour) + 12

    # Return the time
    return f'{hour}:{min}'

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
        'sNUM': entry['sNUM'],
        'term': entry['term'],
        'campus': entry['campus'],
        'online': entry['online'],
        'startTime': extractTime(entry['startTime']),
        'endTime': extractTime(entry['endTime']),
        'days': entry['days'],
        'building': entry['building'],
        'room': entry['room'],
        'startDate': entry['startDate'],
        'endDate': entry['endDate'],
        'cType': entry['cType'],
        'instructors': entry['instructors']
    }


    return


print("classes: ", len(classes))
print("keys: ", classes[0].keys())

i=0
for c in classes[:100]:
    raw = c['startTime']
    time = extractTime(raw)
    print(i, time, raw)
    i+=1



def insertClass():
    return

def insertTerm():
    return

