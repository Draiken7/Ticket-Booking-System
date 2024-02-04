from functools import wraps
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask import request, jsonify

from models import Users

# Creating a decorator for applying role based access control
def rbac_required(required_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()  # Verify that a valid JWT is present in the request
            current_user_name = get_jwt_identity()  # Get the user name from the JWT
            # print(current_user_name)
            
            # Get the roles associated with the current user
            user_roles = [Users.query.filter(Users.username==current_user_name).first().roles[0].name]
            # print(user_roles)    
                        
            # Check if the user has at least one of the required roles
            if any(role in required_roles for role in user_roles):
                return fn(*args, **kwargs)
            else:
                return jsonify({"message": "Unauthorized"}), 401
        return wrapper
    return decorator

# Creating method for getting username from auth token
def getUser():
    verify_jwt_in_request()
    username = get_jwt_identity()
    return Users.query.filter(Users.username==username).first()

# Other Helper Functions
# Date time related functions
import datetime
def getDate(d):
    temp = d.split('-')
    return datetime.date(int(temp[0]), int(temp[1]), int(temp[2]))

def getTime(d):
    temp = d.split(':')
    return datetime.time(int(temp[0]), int(temp[1]))

def getNow():
    return datetime.date.today()

def timeadd(d, e):
    temp1 = d.split(':')
    temp2 = e.split(':')
    return datetime.time(int(temp1[0])+int(temp2[0]), int(temp1[1])+int(temp2[0]))

def dateadd(d, e):
    for i in range(e):
        d = loopday(d)
    return datetime.datetime.combine(d, datetime.time(0, 0))
    
def loopday(d):
    try:
        a = datetime.date(d.year, d.month, d.day+1)
        return a
    except ValueError:
        try:
            a = datetime.date(d.year, d.month + 1, 1)
            return a
        except ValueError:
            a = datetime.date(d.year + 1, 1, 1)
            return a
        
def gettoday(isdatetime = False):
    if isdatetime:
        return datetime.datetime.combine(datetime.date.today(), datetime.time(0,0))
    return datetime.date.today()

def getnowDateTime():
    return datetime.datetime.now()

def pastMonth():
    now = datetime.datetime.now()
    if now.month == 1:
        y = now.year - 1
        return datetime.datetime(y, 12, now.day, now.hour, now.minute)
    m = now.month - 1
    return datetime.datetime(now.year, m, now.day, now.hour, now.minute)