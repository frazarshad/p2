from item import Item
import pymysql
from random import Random


class DBHandler:

    def __init__(self, DATABASEIP, DB_PORT, DB_USER, DB_PASSWORD, DATABASE):
        self.DB_HOST = DATABASEIP
        self.DB_PORT = DB_PORT
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DATABASE = DATABASE

    def signup(self, password, fname):
        db = None
        cur = None
        insert = False
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cur = db.cursor()
            sql = 'INSERT INTO users (password, username) VALUES (%s, %s)'
            args = (password, fname)
            cur.execute(sql, args)
            insert = True

        except Exception as e:
            print(e)
        finally:
            if db is not None:
                db.commit()
            cur.close()
            db.close()
            return insert

    def login(self, password, name):
        db = None
        cursor = None
        found = False
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cursor = db.cursor()
            sql = 'SELECT * FROM users WHERE username=%s AND password=%s'
            args = (name, password)
            cursor.execute(sql, args)
            if cursor.arraysize == 1:
                found = True
        except Exception as e:
            print(e)
        finally:
            if db:
                db.commit()
                cursor.close()
                db.close()
            return found

    def showUsers(self, fname):
        db = None
        cursor = None
        myList = []
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD, database=self.DATABASE)
            cur = db.cursor()
            print("here")
            sql = 'Select fname, lname, email from users where fname ='+'%s'
            args = fname
            cur.execute(sql, args)
            user = ""

            for row in cur.fetchall():
                user += "fname:"+row[0]
                user += "lname:" + row[1]
                user += "email:" + row[2]
                myList.append(user)

        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db is not None:
                db.commit()

            return myList

    def generate_serial(self):
        rand = Random()
        rand.seed()
        serial = ""
        for i in range(0, 10):
            serial += str(rand.randint(0, 9))
        return serial

    def store_item(self, item):
        cursor = None
        db = None
        serial = None
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cursor = db.cursor()
            query = "INSERT INTO items (serial, title, color, quantity, category, gender, price, manufacturer)" + \
                    f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            added = False
            while not added:
                try:
                    serial = self.generate_serial()
                    cursor.execute(query, [serial]+item)
                    added = True
                except:
                    pass

            db.commit()
            return serial
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    def get_items(self, color='%', gender='%', category='all', price_start=0, price_end=100000, sort_by='date_added DESC'):
        category = '%' if category == 'all' else category
        cursor = None
        db = None
        items = []

        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cursor = db.cursor()
            query = "SELECT * FROM items WHERE color LIKE %s AND gender LIKE %s AND category LIKE %s AND price>=%s " \
                    "AND price<=%s ORDER BY " + sort_by
            cursor.execute(query, [color, gender, category, price_start, price_end])
            for item in cursor.fetchall():
                items.append(Item(*item))

            return items
        except Exception as e:
            print(e)
            return []
        finally:
            cursor.close()
            db.close()

    def delete_item(self, serial):
        cursor = None
        db = None
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cursor = db.cursor()
            query = "DELETE FROM items WHERE serial=%s;"
            cursor.execute(query, serial)
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def change_item(self, serial, item):
        cursor = None
        db = None
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cursor = db.cursor()
            query = "UPDATE items SET title=%s, color=%s, quantity=%s, category=%s, gender=%s, price=%s," \
                    " manufacturer=%s WHERE serial=%s"
            cursor.execute(query, item + [serial])
            db.commit()
            return True
        except Exception as e:
            print(e)
            return False
        finally:
            cursor.close()
            db.close()

    def item_detail(self, serial):
        cursor = None
        db = None
        items = []
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cursor = db.cursor()
            query = "SELECT * FROM items WHERE serial LIKE %s"
            args = (serial)
            cursor.execute(query,args)
            for item in cursor.fetchall():
                items.append(Item(*item))
            return items

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

            return myList

    def get_top_bought_items(self):
        cursor = None
        db = None
        items = []
        try:
            db = pymysql.connect(host=self.DB_HOST, port=self.DB_PORT, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cursor = db.cursor()
            query = "SELECT * FROM items ORDER BY bought DESC LIMIT 6"
            cursor.execute(query)

            for item in cursor.fetchall():
                items.append(Item(*item))
            return items
        except Exception as e:
            print(e)
            return []
        finally:
            cursor.close()
            db.close()


def Test():
    db = DBHandler("localhost", "root", "nimra","testdb")
    mylist = db.showUsers("test")
    for i in mylist:
        print(i)


if __name__ == '__main__':
    Test()





