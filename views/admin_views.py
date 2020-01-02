from flask import Blueprint, request, redirect, render_template, current_app
import os

from item import Item
from DBHandler import DBHandler

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin')
def admin_page():
    if request.cookies['user']:  #== 'admin':
        db = DBHandler(current_app.config['DATABASEIP'], current_app.config['PORT'], current_app.config['DB_USER'],
                       current_app.config['DB_PASSWORD'], current_app.config['DATABASE'])
        items = db.get_items()
        from app import lists
        return render_template('admin.html', item=items, lists=lists)
    else:
        return redirect('/')


@admin.route('/admin_add_item', methods=['POST'])
def admin_add_item():
    if len(request.form) != 0:
        item = Item(
            request.form.get('title'),
            request.form.get('color'),
            request.form.get('quantity'),
            request.form.get('category'),
            request.form.get('gender'),
            request.form.get('price'),
            request.form.get('manufacturer'),
        )
        db = DBHandler(current_app.config['DATABASEIP'], current_app.config['PORT'], current_app.config['DB_USER'],
                       current_app.config['DB_PASSWORD'], current_app.config['DATABASE'])
        serial_number = db.store_item(item)
        if serial_number is not None:
            file = request.files['picture']
            file_extension = file.filename.split('.')[-1]

            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], '.'.join([serial_number, file_extension])))
        else:
            pass
            # do something for error
    return redirect('/admin')
