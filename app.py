from flask import Flask, request,make_response, render_template
from DBHandler import DBHandler

abc = Flask(__name__)
abc.config.from_object('config')



@abc.route('/')
@abc.route('/hell')
def hello_world():
    return render_template("login.html")

def test():
    return "My Hello"
abc.add_url_rule("/test","tt",test)
@abc.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    db = None
    try:
        print("Test")
        password = request.form['password']
        fname = request.form['fname']
        print(abc.config["DATABASEIP"])
        db = DBHandler(abc.config["DATABASEIP"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                       abc.config["DATABASE"])
        done = db.signup(password, fname)
        print(done)
        resp=make_response(render_template('mytemplate.html', done=done, name=fname))
        resp.set_cookie('user',fname)
        return resp

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('login.html', error=error)

@abc.route("/login",methods=['POST','GET'])
def login():
    error = None
    db = None
    try:
        print("Test")
        password = request.form['password']
        name = request.form['name']
        print(abc.config["DATABASEIP"])
        db = DBHandler(abc.config["DATABASEIP"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                       abc.config["DATABASE"])
        done = db.login(password, name)
        print(done)
        return render_template('mytemplate.html', done=done, name=name)

    except Exception as e:
        print(e)
        error = str(e)
        return render_template('login.html', error=error)



if __name__ == '__main__':
    abc.run()
