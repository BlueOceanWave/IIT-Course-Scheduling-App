import psycopg2

# connect to PostgreSQL database
connection = psycopg2.connect(
    dbname='NewDB',
    user='postgres',
    password='123456',
    host='localhost',
    port='5432'
)


def getEntry(name):
    # create a cursor to interact with the database
    cursor = connection.cursor()

    query = "SELECT * FROM persons WHERE name = %s"  # define the query
    match_val = name

    cursor.execute(query, (match_val,))

    row = cursor.fetchone()

    cursor.close()
    return row[1]

def newEntry(name, password):
    cursor = connection.cursor()
    query = "INSERT INTO persons (name, password) VALUES (%s, %s)"
    values = (name, password)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    print("Successful row insert")

def searchEntry(name):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM persons WHERE name = %s)"
    match_val = name
    cursor.execute(query, (match_val,))
    result = cursor.fetchone()
    cursor.close()
    return result[0]
