from lists import lists
from flask import Blueprint, request, redirect, render_template, current_app, url_for
import os

from item import Item
from DBHandler import DBHandler

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin')
def admin_page():
    # if request.cookies.get('user') != 'admin':
    #   return redirect('/')

    db = DBHandler(current_app.config['DATABASEIP'], current_app.config['PORT'], current_app.config['DB_USER'],
                   current_app.config['DB_PASSWORD'], current_app.config['DATABASE'])
    items = db.get_items()
    return render_template('admin.html', items=items, lists=lists)


@admin.route('/add_item', methods=['POST'])
def admin_add_item():
    if request.cookies.get('user') != 'admin':
        return redirect('/')

    try:
        item = [
            request.form.get('title'),
            request.form.get('color'),
            int(request.form.get('quantity')),
            request.form.get('category'),
            request.form.get('gender'),
            float(request.form.get('price')),
            request.form.get('manufacturer'),
        ]
        if validate_form_data(item) and \
                request.files['picture'].content_type != 'images/png':
            db = DBHandler(current_app.config['DATABASEIP'], current_app.config['PORT'], current_app.config['DB_USER'],
                           current_app.config['DB_PASSWORD'], current_app.config['DATABASE'])
            serial_number = db.store_item(item)
            if serial_number is not None:
                file = request.files['picture']
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], serial_number + ".png"))
            else:
                pass
                # do something for error
        else:
            return redirect('/admin?invalid=True')
    except Exception as e:
        print(e)
        return redirect('/admin?invalid=True')

    return redirect('/admin')


@admin.route("/delete/<serial>")
def delete(serial):
    if request.cookies.get('user') != 'admin':
        return redirect('/')

    try:
        int(serial)  # Checking if the serial is a number
        db = DBHandler(current_app.config['DATABASEIP'], current_app.config['PORT'], current_app.config['DB_USER'],
                       current_app.config['DB_PASSWORD'], current_app.config['DATABASE'])
        db.delete_item(serial)
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], serial + ".png"))
    finally:
        return redirect('/admin')


@admin.route("/edit_item/<serial>", methods=['POST'])
def edit_item(serial):
    if request.cookies.get('user') != 'admin':
        return redirect('/')

    try:
        int(serial)
        item = [
            request.form.get('title'),
            request.form.get('color'),
            int(request.form.get('quantity')),
            request.form.get('category'),
            request.form.get('gender'),
            float(request.form.get('price')),
            request.form.get('manufacturer'),
        ]
        if validate_form_data(item):
            db = DBHandler(current_app.config['DATABASEIP'], current_app.config['PORT'], current_app.config['DB_USER'],
                           current_app.config['DB_PASSWORD'], current_app.config['DATABASE'])
            db.change_item(serial, item)
            if request.files['picture'].filename != '' and request.files['picture'].content_type != 'images/png':
                file = request.files['picture']
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], serial + ".png"))
            else:
                pass
                # do something for error

            return redirect('/admin')
        else:
            return redirect('/admin?invalid=True')  # add some form of reply with 'invalid form data'
    except Exception as e:
        print(e)
        return redirect('/admin?invalid=True')


def validate_form_data(item):
    """Checks validity of the form data"""
    for field in item:
        if field == '':
            return False

    if len(item[0]) > 30 or \
            item[1] not in lists['colors'] or \
            item[2] < 1 or \
            item[4] not in lists['genders'] or \
            item[3] not in lists[item[4] + '_categories'] or \
            item[5] < 0.0:
        return False

    return True

