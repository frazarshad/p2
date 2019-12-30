from flask import Blueprint, request, redirect, render_template, current_app
import os

from item import Item
from DBHandler import DBHandler

admin = Blueprint('admin', __name__, template_folder='templates')


@admin.route('/admin')
def admin_page():
    if request.cookies['user'] == 'admin':
        return render_template('admin.html')
    else:
        return redirect('/')


@admin.route('/admin_add_item', methods=['POST'])
def admin_add_item():
    try:
        item = Item(
            request.form.get('serial'),
            request.form.get('title'),
            request.form.get('color'),
            request.form.get('quantity'),
            request.form.get('category'),
            request.form.get('gender'),
            request.form.get('price'),
            request.form.get('manufacturer'),
        )
        file = request.files['picture']
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
    except:
        return redirect('/admin')
