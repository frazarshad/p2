import pymysql


class DBHandler:

    def __init__(self, DATABASEIP, DB_PORT, DB_USER, DB_PASSWORD, DATABASE):
        self.DB_HOST = DATABASEIP
        self.DB_PORT = DB_PORT
        self.DB_USER = DB_USER
        self.DB_PASSWORD = DB_PASSWORD
        self.DATABASE = DATABASE

    def __del__(self):
        print("Destructor")

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
        insert = False
        try:
            db = pymysql.connect(host=self.DB_HOST, port=3307, user=self.DB_USER, passwd=self.DB_PASSWORD,
                                 database=self.DATABASE)
            cur = db.cursor()
            print("here")
            sql = 'SELECT * FROM users WHERE username=%s AND password=%s'
            args = (name, password)
            cur.execute(sql, args)
            name, password = cur.fetchone();
            if name is None:
                insert = False
            else:
                insert = True
        except Exception as e:
            print(e)
            print("some error")
        finally:
            if db is None:
                db.commit()
                db.commit()
            return cur

    def showUsers(self, fname):
        db = None
        cursor = None
        myList = []
        try:
            db = pymysql.connect(host=self.DB_HOST, port=3307, user=self.DB_USER, passwd=self.DB_PASSWORD, database=self.DATABASE)
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


def Test():
    db = DBHandler("localhost", "root", "nimra","testdb")
    mylist = db.showUsers("test")
    for i in mylist:
        print(i)


if __name__ == '__main__':
    Test()





