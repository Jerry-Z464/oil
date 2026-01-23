class CustomException(Exception):
    pass


def is_null(obj):
    """If the object is null, return True, else return False."""
    return obj is None


def non_null(obj):
    """If the object is not null, return True, else return False."""
    return obj is not None


def is_blank(s):
    """If the string is null or empty,
    or the content is all spaces, or the content is 'null', return True, else return False."""
    return is_null(s) or not s.strip() or s.lower() == "null"


def non_blank(s):
    """If the string is not blank, return True."""
    return not is_blank(s)


def is_empty(obj):
    """Check if Array, Collection, or Map is empty."""
    if obj is None:
        return True

    if isinstance(obj, (list, tuple)):
        return len(obj) == 0
    if isinstance(obj, dict):
        return len(obj) == 0
    if isinstance(obj, str):
        return obj == "" or obj.lower() == "null"

    return False


def non_empty(obj):
    """If the object is not empty, return True."""
    return not is_empty(obj)


