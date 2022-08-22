"""This function appends a copple key/value to a dictionary"""


def append_value(dict_obj, key, value):
    # check if key exist in dict or not
    if key in dict_obj:
        # key exist in dict
        # check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # append the value in list
        dict_obj[key].append(value)
    else:
        # as key is not in dict,
        # so, add key-value pair
        dict_obj[key] = [value]
