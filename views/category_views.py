from DBHandler import DBHandler
from flask import Blueprint, current_app, redirect, render_template, request, url_for
from lists import lists

category = Blueprint('category', __name__)

@category.route('/category')
def blank_category_page():
    return redirect(url_for('category.category_page', gender='all', category_='all', page_no=1))


@category.route('/category/<gender>')
def gender_category_page(gender):
    return redirect(url_for('category.category_page', gender=gender, category_='all', page_no=1))


@category.route('/category/<gender>/<category_>')
def page_category_page(gender, category_):
    return redirect(url_for('category.category_page', gender=gender, category_=category_, page_no=1))


@category.route('/category/<gender>/<category_>/<int:page_no>')
def category_page(gender, category_, page_no):
    sort_list = {'new': 'date_added DESC', 'a-z': 'title ASC', 'z-a': 'title DESC', 'low-high': 'price ASC',
                 'high-low': 'price DESC'}

    color = request.args.get('color') if request.args.get('color') else '%'
    show = int(request.args.get('show')) if request.args.get('show') else 12
    price_start = int(request.args.get('start_amount')) if request.args.get('start_amount') else 0
    price_end = int(request.args.get('end_amount')) if request.args.get('end_amount') else 100000
    sort_by = sort_list[request.args.get('sort_by')] if request.args.get('sort_by') else sort_list['new']

    # Checking whether all values provided are correct
    if (gender not in lists['genders'] and gender != 'all') or \
            (category_ not in lists[gender + '_categories'] and category_ != 'all'):
        return redirect(url_for('category.blank_category_page'))

    db = DBHandler(current_app.config['DATABASEIP'], current_app.config['PORT'], current_app.config['DB_USER'],
                   current_app.config['DB_PASSWORD'], current_app.config['DATABASE'])
    items = db.get_items(color, gender, category_, price_start, price_end, sort_by)
    upper_limit = show * page_no
    lower_limit = upper_limit - show

    return render_template('category.html', lists=lists, page_name='category', gender_main=gender, category_main=category_,
                           page_no_main=page_no, items=items[lower_limit:upper_limit], pages=int((len(items)/show)+1),
                           show=show, start_amount=price_start, end_amount=price_end, sort_by=sort_by)