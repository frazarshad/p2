from flask import Flask, request, make_response, render_template, redirect
from DBHandler import DBHandler

from views.admin_views import admin
from views.category_views import category

# lists has been moved to lists.py

abc = Flask(__name__, template_folder='templates')
abc.config.from_object('config')

abc.register_blueprint(admin)
abc.register_blueprint(category)


@abc.route('/')
def index():
    db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                   abc.config["DATABASE"])
    items = db.get_top_bought_items()
    return render_template("index.html", items=items)


@abc.route('/signup', methods=['POST', 'GET'])
def signup():
    error = None
    try:
        print("Test")
        password = request.form['password']
        fname = request.form['fname']
        print(abc.config["DATABASEIP"])
        db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                       abc.config["DATABASE"])
        done = db.signup(password, fname)
        print(done)
        resp = make_response(render_template('mytemplate.html', done=done, name=fname))
        resp.set_cookie('user', fname)
        return resp

    except Exception as e:
        return render_template('signup.html', error=error)


@abc.route("/login", methods=['POST'])
def login():
    if request.cookies.get('user'):
        return redirect('/')

    if len(request.form) != 0:
        password = request.form['password']
        name = request.form['name']
        db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                       abc.config["DATABASE"])
        done = db.login(password, name)

        if done:
            resp = make_response(redirect('/'))
            resp.set_cookie('user', name)
            return resp
        else:
            return render_template('login.html', login_failed=True)
    else:
        return render_template('login.html', login_failed=False)


@abc.route("/logout")
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('user', '\0', max_age=0)
    return redirect('/login')


@abc.route("/browsing/<serial>")
def detail(serial):
        int(serial)
        db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                   abc.config["DATABASE"])
        done = db.item_detail(serial)
        if done is None:
            return redirect('/browsing')
        else:
            return render_template('detail.html', item=done, serial=serial)


@abc.route("/during_detail/<serial>")
def during_detail(serial):
    resp = make_response(redirect('/'))

    resp.set_cookie('serial', (request.cookies.get('serial') + ':' if request.cookies.get('serial') else '') + serial)
    return resp


@abc.route("/contact_us")
def contact():
    return render_template('contact.html')


if __name__ == '__main__':
    abc.run()
