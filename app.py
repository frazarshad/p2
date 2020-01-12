from flask import Flask, request, make_response, render_template, redirect
from DBHandler import DBHandler
from item import Item
from views.admin_views import admin
from views.category_views import category

from lists import lists
# lists has been moved to lists.py

abc = Flask(__name__, template_folder='templates')
abc.config.from_object('config')

abc.register_blueprint(admin)
abc.register_blueprint(category)


@abc.context_processor
def base_variables():
    if request.cookies.get('serial'):
        cart = request.cookies.get('serial').split(':')
    else:
        cart = []

    db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                   abc.config["DATABASE"])
    cart_items = [db.item_detail(serial) for serial in cart]
    return dict(lists=lists, cookies=request.cookies, cart_items=cart_items)


@abc.route('/')
def index():
    db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                   abc.config["DATABASE"])
    items = db.get_top_bought_items()
    return render_template("index.html", items=items)


@abc.route('/signup', methods=['POST', 'GET'])
def signup():
    try:
        password = request.form['password']
        name = request.form['name']
        db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                       abc.config["DATABASE"])
        done = db.signup(password, name)
        if done:
            resp = make_response(redirect('/'))
            resp.set_cookie('user', name)
            return resp
        else:
            return render_template('signup.html')

    except Exception as e:
        return render_template('signup.html')


@abc.route("/login", methods=['POST', 'GET'])
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
            resp = make_response(redirect('/admin' if name == 'admin' else '/'))
            resp.set_cookie('user', name)
            return resp
        else:
            return render_template('login.html', login_failed=True)
    else:
        return render_template('login.html', login_failed=False)


@abc.route("/logout")
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('user', '\0', expires=0)
    return response


@abc.route("/browsing/<serial>")
def detail(serial):
    db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                   abc.config["DATABASE"])
    done = db.item_detail(serial)
    if done is None:
        return redirect('/browsing')
    else:
        return render_template('single-product.html', item=done, serial=serial)


@abc.route("/during_detail/<serial>")
def during_detail(serial):
    resp = make_response(redirect(request.referrer))

    resp.set_cookie('serial', (request.cookies.get('serial') + ':' if request.cookies.get('serial') else '') + serial)
    return resp


@abc.route("/contact_us", methods=['POST', 'GET'])
def contact():
    if len(request.form) != 0:
        message = request.form.get('message')
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')

        db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                        abc.config["DATABASE"])
        db.store_message(message=message, name=name, email=email, subject=subject)
        return render_template('message-sent.html')
    return render_template('contact.html')


@abc.route("/about")
def about():
    return render_template('about.html')


@abc.route('/cart')
def cart():
    serials = []
    item = []
    count = 0
    serials = request.cookies.get("serial").split(":")
    db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                   abc.config["DATABASE"])
    for x in serials:
        done = db.item_detail(x)
        item.append(done)
        count = count + done.price

    return render_template("cart.html", item=item)


@abc.route('/search', methods=['POST'])
def search():
    if request.form.get('search_input'):
        to_search = request.form.get('search_input')
        db = DBHandler(abc.config["DATABASEIP"], abc.config["PORT"], abc.config["DB_USER"], abc.config["DB_PASSWORD"],
                       abc.config["DATABASE"])
        items = db.search(to_search)
        return render_template('search-results.html', items=items, to_search=to_search)
    else:
        return redirect('/')

if __name__ == '__main__':
    abc.run()
