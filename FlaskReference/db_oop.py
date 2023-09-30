import psycopg2

# This is my attemp at making an object-oriented approach at communicating with the database
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
            print("Username not in database")
            return
    
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

