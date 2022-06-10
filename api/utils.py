from django.db import connection

def keyExistAndLength(obj, key, minLength):
    try:
        if key in obj :
            if len(obj[key]) >= minLength:
                return True
    except:
        return False
