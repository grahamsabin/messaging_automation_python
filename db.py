# from app import app
import pymysql.cursors
import os


DB_host = os.getenv('CLEARDB_HOST')
DB_user = os.getenv('CLEARDB_USER')
DB_password = os.getenv('CLEARDB_PASSWORD')
DB_database = os.getenv('CLEARDB_DATABASE')
print(DB_host)
print(DB_user)
print(DB_password)
print(DB_database)
# Connect to the database
mysql = pymysql.connect(host=DB_host,  # potentially change the name back to 'connection'
                             user=DB_user,
                             password=DB_password,
                             database=DB_database,
                             cursorclass=pymysql.cursors.DictCursor)

#you need to run the full application in order for this to show up

# mysql = pymysql.connect(host='us-cdbr-east-06.cleardb.net', # potentially change the name back to 'connection'
#                             user='b78cc361f81387',
#                             password='ec7976d2',
#                             database='heroku_5717474ee527107',
#                             cursorclass=pymysql.cursors.DictCursor)

with mysql:
    with mysql.cursor() as cursor:
        sql = "INSERT INTO `users` (`name`, `phone_number`, `password`) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('test 5', '4255537651', 'testpass'))
        mysql.commit()
        print('this ran')

    with mysql.cursor() as cursor:
        sql = "SELECT `id`, `password` FROM `users` WHERE `phone_number`=%s"
        cursor.execute(sql, ('4255537651',))
        result = cursor.fetchone()
        print(result)

# mysql://b78cc361f81387:ec7976d2@us-cdbr-east-06.cleardb.net/heroku_5717474ee527107?reconnect=true





