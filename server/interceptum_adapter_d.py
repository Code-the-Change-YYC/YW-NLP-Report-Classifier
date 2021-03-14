import json

with open('interceptum_form_codes.json') as f:
    form_codes = json.load(f)

interceptum_boolean_dict = {True: "1", False: "2"}

field_values_dict = form_codes['field_values_dict']

multi_options = form_codes['multi_options']

single_option = form_codes['single_options']
