# utilities.py

from datetime import datetime

def is_empty_or_whitespace(s):
    return s is None or s.strip() == ""

def is_valid_date_format(s):
    try:
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False
