import psycopg2

# This is the simplest way I can make a python file communicate with a databse. 
# These are all just functions that make the code get values from the database.

# Still unfinished.

# connect to PostgreSQL database
connection = psycopg2.connect(
    dbname='NewDB',
    user='postgres',
    password='123456',
    host='localhost',
    port='5432'
)


# Gets an entry give the name of the row (to be updated for the ipro db)
def getEntry(name):
    # create a cursor to interact with the database
    cursor = connection.cursor()

    query = "SELECT * FROM persons WHERE name = %s"  # define the query
    match_val = name

    cursor.execute(query, (match_val,))

    row = cursor.fetchone()

    cursor.close()
    return row[1]

# Creates a new entry given the name and password (to be updated for the ipro db)
def newEntry(name, password):
    cursor = connection.cursor()
    query = "INSERT INTO persons (name, password) VALUES (%s, %s)"
    values = (name, password)
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    print("Successful row insert")

# Checks if an entry exists in the database (to be updated for the ipro db)
def searchEntry(name):
    cursor = connection.cursor()
    query = "SELECT EXISTS(SELECT 1 FROM persons WHERE name = %s)"
    match_val = name
    cursor.execute(query, (match_val,))
    result = cursor.fetchone()
    cursor.close()
    return result[0]
