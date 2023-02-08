def set_function_attributes(**kwargs):
    def decorator(func):
        for key, val in kwargs.items():
            setattr(func, key, val)

        return func

    return decorator


def normalize_townname(townname):
    return townname.replace("台", "臺")

def translate_array_of_integer(translate_dict, array_of_integer): 
    if isinstance(array_of_integer, list):
        return ", ".join(translate_dict.get(item, str(item)) for item in array_of_integer)

    return ""
