# import mysql.connector

# def create_connection():
#     db_connection = mysql.connector.connect(host='192.241.152.37',
#                                             user='root',
#                                             password='leaflykids',
#                                             database='BestBud')
#     return db_connection

# def select_test():
#     connection = create_connection()
#     cursor = connection.cursor()

#     cursor.execute('SELECT * FROM strains')

#     result = cursor.fetchall()

#     connection.close()

#     return result