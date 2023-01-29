import psycopg2

def db_connect():
    try:
        connection = psycopg2.connect(database='postgres', user = 'postgres', password = '123456', host = 'localhost', port= '5432')
        # print('database connection established')
        cursor = connection.cursor()
        return connection, cursor
    except Exception  as e:
        # print("database cannot connect")
        return e