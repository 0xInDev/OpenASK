from django.db import connection

def keyExistAndLength(obj, key, minLength):
    try:
        if key in obj :
            if len(obj[key]) >= minLength:
                return True
    except:
        return False

class ErrorCode:
    SONDAGE_ID_MISSING = 10001
    SONDAGE_PERSON_INFORMATION_MISSING = 10002
    SONDAGE_PERSON_EMAIL_MISSING = 10003
    SONDAGE_RESPONSE_MISSING = 10004

    SONDAGE_PERSON_ALREADY_REPLY = 10005
    SONDAGE_QUESTION_NOT_EXIST = 10006
    SONDAGE_BAD_QUESTION_RESPONSE_TYPE = 10007