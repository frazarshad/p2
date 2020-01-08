# a dictionary that contains important lists such as colors and categories of items. these can then be imported
# to quickly create lists and selection inputs in html
lists = {
    'male_categories': ['shirts', 'jeans', 'shoes', 'sweaters'],
    'female_categories': ['shirts', 'jeans', 'shoes', 'bags'],
    'child_categories': ['shirts', 'jeans', 'shoes'],
    'all_categories': None,  # empty for now will fill on next line
    'colors': ['black', 'blue', 'gray', 'red', 'yellow'],
    'genders': ['male', 'female', 'child']
}
lists['all_categories'] = list(set(lists['female_categories']) | set(lists['male_categories']))