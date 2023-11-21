import psycopg2
import json, bcrypt
from datetime import time

salt =  b'$2b$12$Hw.Vq/gUQ1/0s37Wep3xP.'

# This is my attempt at making an object-oriented approach at communicating with the database
# The goal is to make a user object, and link it to the database.

# Still a work in progress.

# connect to PostgreSQL database
connection = psycopg2.connect(
    dbname='NewDB',
    user='postgres',
    password='123456',
    host='localhost',
    port='5432'
)

class student_account:
    table = "accounts"
    username = ""
    password = ""
    major = ""

    def __init__(self, un="", pswd="", mjr=""):
        self.username = un
        # self.password = bcrypt.hashpw(pswd.encode('utf-8'), salt).decode('utf-8')
        self.password = pswd
        self.major = mjr
        
    def insertToDB(self):
        cursor = connection.cursor()
        query = f"INSERT INTO {self.table} (username, password, major) VALUES (%s, %s, %s)"
        values = (self.username, self.password, self.major)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print("Successful row insert")
        
    def isInDB(self):
        cursor = connection.cursor()
        query = f"SELECT COUNT(*) FROM {self.table} WHERE username = %s AND password = %s;"
        values = (self.username, self.password)
        cursor.execute(query, values)
        result = cursor.fetchone()
        cursor.close()
        if result[0] == 0:
            return False
        else:
            return True
    
    def getFromDB(self):
        exists = self.isInDB()
        if exists:
            cursor = connection.cursor()
            query = f"SELECT major FROM {self.table} WHERE username = %s AND password = %s"
            values = (self.username, self.password)
            cursor.execute(query, values)
            major = cursor.fetchone()[0]
            return student_account(self.username, self.password, major)
        else:
            print("Account not in database")
            return None
        
    def getFromDBWOPassword(self):
        exists = self.searchEntry(self.username)
        if exists:
            cursor = connection.cursor()
            query = f"SELECT major, password FROM {self.table} WHERE username = %s"
            values = (self.username,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            major = result[0]
            password = result[1]
            print(self.username, major, password)
            return student_account(self.username, password, major)
        else:
            print("Account not in database")
            return None
        

    def searchEntry(self, name):
        cursor = connection.cursor()
        query = "SELECT EXISTS(SELECT 1 FROM accounts WHERE username = %s)"
        match_val = name
        cursor.execute(query, (match_val,))
        result = cursor.fetchone()
        cursor.close()
        return result[0]
    
    def getPassword(self):
        exists = self.searchEntry(self.username)
        if exists:
            return self.password
        else:
            print("Password not in database")
            return
    
    def getMajor(self):
        exists = self.searchEntry(self.major)
        if exists:
            return self.major
        else:
            print("Major not in database")
            return
        
    def changeInfo(self, old_username, new_username, new_password, new_major):
        cursor = connection.cursor()
        if new_password != "":
            query = f"""
                UPDATE {self.table}
                SET username = %s, password = %s, major = %s
                WHERE username = %s;
            """
            values = (new_username, new_password, new_major, old_username)
            cursor.execute(query, values)
            connection.commit()
        else:
            print("blank new password")
            query = f"""
                UPDATE {self.table}
                SET username = %s, major = %s
                WHERE username = %s;
            """
            values = (new_username, new_major, old_username)
            cursor.execute(query, values)
            connection.commit()
        cursor.close()
        return

class classes:
    table = "classes"
    crn = ""
    sid = ""
    cid = ""
    snum = ""
    term = ""
    days = ""
    starttime = ""
    endtime =""
    campus = ""
    online = ""
    building = ""
    room = ""

    def __init__(self, crn="", sid="", cid="", snum="", term="", days="", starttime="", endtime="", campus="", online="", building="", room=""):
        self.crn = crn
        self.sid = sid
        self.cid = cid
        self.snum = snum
        self.term = term
        self.days = days
        self.starttime = starttime
        self.endtime = endtime
        self.campus = campus
        self.online = online
        self.building = building
        self.room = room

def getAllClasses():
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM classes;")
        rows = cursor.fetchall()  # fetch all the rows from the table
        # Get the column names for dictionary keys
        column_names = [desc[0] for desc in cursor.description]
        data = []
        for row in rows:
            row_dict = dict(zip(column_names, row))  # turn each row into a dictionary
            # Convert time objects to string representations
            if row_dict['starttime'] is not None:
                row_dict['starttime'] = row_dict['starttime'].strftime('%H:%M:%S')
            if row_dict['endtime'] is not None:
                row_dict['endtime'] = row_dict['endtime'].strftime('%H:%M:%S')
            data.append(row_dict)  # append them to the data list
        # Serialize the data to JSON
        json_data = json.dumps(data, default=str)  # Use default=str to serialize other non-serializable objects as strings
        return json_data
    except psycopg2.Error as e:
        # Handle database connection or query errors here
        print("Error:", e)
        return None
    finally:
        if connection:
            connection.close()


def insertToTaken(username, sid, cid):
    cursor = connection.cursor()
    checkQuery = "SELECT 1 FROM taken WHERE (username = %s AND sid = %s AND cid = %s)"
    cursor.execute(checkQuery, [username, sid, cid])
    if(not cursor.fetchone()):
        query = f"INSERT INTO taken (username, sid, cid) VALUES (%s, %s, %s)"
        values = (username, sid, cid)
        cursor.execute(query, values)
        connection.commit()
        cursor.close()
        print("Taken class added for ", username)
        return True, "Added To Taken"
    return False, "Class Already In Taken"

def deleteFromTaken(username, sid, cid):
    cursor = connection.cursor()
    checkQuery = "SELECT 1 FROM taken WHERE (username = %s AND sid = %s AND cid = %s)"
    cursor.execute(checkQuery, [username, sid, cid])
    if(cursor.fetchone()):
        query = "DELETE FROM taken WHERE (username = %s AND sid = %s AND cid = %s)"
        print("HELLO " + username,sid,cid)
        cursor.execute(query, [username, sid, cid])
        connection.commit()
        cursor.close()
        print("Taken class deleted for ", username)
        return True, "Deleted From Taken"
    return False, "Class Doesnt Exist"

def getTakenCourses(username):
    cursor = connection.cursor()
    query = f"SELECT sid, cid FROM taken WHERE username = %s"
    values = (username,)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    print("Got course/s ", result, " for ", username)
    return [result]


def insertToSchedules(username, crn, sindex):
    cursor = connection.cursor()
    query = f"INSERT INTO schedules (username, crn, sindex) VALUES (%s, %s, %s)"
    values = (username, crn, sindex)
    

    try:
        cursor.execute(query, values)
        connection.commit()
        print("class added to ", username, "'s schedule")
        return True
    except: 
        connection.rollback()
        print("Error adding class to ", username, "'s schedule")
        return False
    finally:
        cursor.close()

def deleteFromSchedule(username, crn, sindex):
    cursor = connection.cursor()
    query = f"DELETE FROM schedules WHERE (username = %s AND crn = %s AND sindex = %s)"
    values = (username, crn, sindex)

    try:
        cursor.execute(query, values)
        connection.commit()
        print("class deleted from ", username, "'s schedule")
        return True
    except: 
        connection.rollback()
        print("Error deleting class from ", username, "'s schedule")
        return False
    finally:
        cursor.close()
    

def getSchedule(username, sindex):  # only gives crns for now; must be modified to give more details other than just crns
    cursor = connection.cursor()
    query = f"SELECT crn, sid, cid, starttime, endtime, days\
            FROM schedules INNER JOIN classes USING (crn) INNER JOIN courses USING (sid, cid)\
            WHERE username = %s AND sindex = %s"
    values = (username, sindex)
    cursor.execute(query, values)
    result = cursor.fetchall()
    cursor.close()
    print("Got schedule ", sindex, " for ", username)
    return result