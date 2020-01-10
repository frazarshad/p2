# a dictionary that contains important lists such as colors and categories of items. these can then be imported
# to quickly create lists and selection inputs in html
lists = {
    'men_categories': ['shirts', 'jeans', 'shoes', 'sweaters'],
    'women_categories': ['shirts', 'jeans', 'shoes', 'bags'],
    'children_categories': ['shirts', 'jeans', 'shoes'],
    'all_categories': None,  # empty for now will fill on next line
    'colors': ['black', 'blue', 'gray', 'red', 'yellow'],
    'genders': ['men', 'women', 'children']
}

lists['all_categories'] = list(set(lists['men_categories']) | set(lists['women_categories']) | set(lists['children_categories']))
