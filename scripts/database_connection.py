import mysql.connector

def create_connection():
     db_connection = mysql.connector.connect(host='192.241.152.37',
                                             user='root',
                                             password='leaflykids',
                                             database='BestBud')
     return db_connection

def execute_select_statement(select_statement):
     connection = create_connection()
     cursor = connection.cursor()

     cursor.execute(select_statement)

     result = cursor.fetchall()

     connection.close()

     return result