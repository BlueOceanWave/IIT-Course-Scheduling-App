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

query = {
    'getInstructors': 'SELECT DISTINCT instructor FROM instructors;',
    'getSubjects': 'SELECT DISTINCT sID AS subject FROM subjects;',

    'getActiveClasses' : 'SELECT * FROM classes INNER JOIN courses INNER JOIN subjects INNER JOIN instructors',
}

cursor = connection.cursor()
cursor.execute('SELECT * FROM classes')
result = cursor.fetchall()
connection.commit()
cursor.close()

print(result)





