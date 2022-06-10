from django.db import connection

def keyExistAndLength(obj, key, minLength):
    try:
        if key in obj :
            if len(obj[key]) >= minLength:
                return True
    except:
        return False

def sqlListQuery( req):
        with connection.cursor() as cursor:
            cursor.execute(req)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
