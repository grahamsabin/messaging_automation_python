# from app import app
import pymysql.cursors





# Connect to the database
mysql = pymysql.connect(host='us-c.cleardb.net', # potentially change the name back to 'connection'
                             user='b78cc361f
                        #add this back from the env file

with mysql:
    with mysql.cursor() as cursor:
        sql = "INSERT INTO `users` (`name`, `phone_number`, `password`) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('test 5', '4255537659', 'testpass'))
        mysql.commit()

    with mysql.cursor() as cursor:
        sql = "SELECT `id`, `password` FROM `users` WHERE `phone_number`=%s"
        cursor.execute(sql, ('4255537659',))
        result = cursor.fetchone()
        print(result)

# mysql://b78cc361f81387:ec7976d2@us-cdbr-east-06.cleardb.net/heroku_5717474ee527107?reconnect=true





