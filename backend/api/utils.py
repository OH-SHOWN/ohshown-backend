def set_function_attributes(**kwargs):
    def decorator(func):
        for key, val in kwargs.items():
            setattr(func, key, val)

        return func

    return decorator


def normalize_townname(townname):
    return townname.replace("台", "臺")

def format_multiple_choice_options(translate_dict, array_of_integer, text_object = {}): 
    if isinstance(array_of_integer, list):
        return ", ".join("%s %s" % (translate_dict.get(item, str(item)), "(%s)" % text_object.get(str(item)) if str(item) in text_object else "") for item in array_of_integer)
    return ""

def format_single_choice_options(translate_dict, integer, text_object = {}): 
    return "%s %s" % (translate_dict.get(integer, str(integer)), "(%s)" % text_object.get(str(integer)) if str(integer) in text_object else "")
