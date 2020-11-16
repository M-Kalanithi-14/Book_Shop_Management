try : import pymysql as cntr
except ImportError : import mysql.connector as cntr

db = cntr.connect(host = 'localhost' , user = 'root' , passwd = 'manager')
cur = db.cursor()

cur.execute('create database book;')
cur.execute('use book')
cur.execute('''create table stock
            (book_id bigint primary key,
            book_name varchar(255),
            book_author varchar(255),
            book_publisher varchar(255),
            book_DoP date,
            book_stock bigint,
            book_rate float);''')
cur.execute('''create table purchase
            (book_id bigint,
            Date date);''')
cur.execute('''create table users
            (name varchar(255) Not Null,
            phone bigint Not Null unique,
            username varchar(255) Not Null,
            password varchar(255) Not Null);''')
cur.execute("insert into users values('kalanithi' , 9486162340 , 'admin' , 'admin@123');")
cur.execute("create unique index book_index on stock(book_id);")
db.commit()
print("Database and Tables created SUCCESSFULLY!!")
c = input("Press any key to continue-------> ")
cur.close()
db.close()