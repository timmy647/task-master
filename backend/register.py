import datetime

from classes import User
from datainteraction import Database
from encode import password_encode
from check_function import *


online_user = []

def register(database: Database, email:str, password:str, name:str):
    if not is_valid_email(email):
        return {"message": "invalid email"}, 400

    if database.is_registered_email(email):
        return {"message": "exist email"}, 400

    if not is_valid_password(password):
        return {"message": "invalid password"}, 400

    if not is_valid_name(name):
        return {"message": "invalid name"}, 400
    user_id = database.get_user_num()
    new_user = User(name, email, password, user_id)
    database.add_new_user(name, email, new_user.get_password())
    online_user.append(new_user)
    return {"message": "register success",
            "token": new_user.get_token()
            }, 200

def login(database: Database, email:str, password:str):
    if not is_valid_email(email):
        return {"message": "invalid email"}, 400

    if not is_valid_password(password):
        return {"message": "invalid password"}, 400

    if not database.is_registered_email(email):
        return {"message": "not exist account"}, 404

    if not database.is_correct_password(email, password_encode(password)):
        return {"message": "email and password not match"}, 400
    else:
        info = database.get_userinfo_from_email(email)
        user = is_oline(info['user_id'], online_user)
        if not user == None:
            online_user.remove(user)
        login_user = User(info['user_name'], email, 'password', info['user_id'])
        online_user.append(login_user)
        return {"message": "login success",
                "token": login_user.get_token()
                }, 200

def logout(token:str):
    logout_user = token_check(token, online_user)
    if logout_user == None:
        return {"message": "authorization error"}, 401

    online_user.remove(logout_user)
    return {"message": "logout success"}, 200

def profile(database: Database, token:str, email:str):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    if type(email) != str:
        return {"message": "email should be string"}, 400
    if not is_valid_email(email):
        return {"message": "email should be email"}, 400
    if not database.is_registered_email(email):
        return {"message": "not exist user"}, 404

    user_info = database.get_userinfo_from_email(email)
    user_id = user_info["user_id"]
    profile_info = database.get_userinfo_from_userid(user_id)

    return {
        "message": "show profile success",
        "profile": profile_info,
    }, 200

def search_profile(database: Database, token:str, email:str):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    if type(email) != str:
        return {"message": "email should be string"}, 400
    if not is_valid_email(email):
        return {"message": "email should be email"}, 400
    if not database.is_registered_email(email):
        return {"message": "not exist user"}, 404

    profile_info = database.get_userinfo_from_email(email)
    return {
               "message": "search profile success",
               "profile": profile_info,
    }, 200

def workload(database:Database, token:str, email:str):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    if type(email) != str:
        return {"message": "email should be string"}, 400
    if not is_valid_email(email):
        return {"message": "email should be email"}, 400
    if not database.is_registered_email(email):
        return {"message": "not exist user"}, 404

    user_info = database.get_userinfo_from_email(email)
    user_id = user_info["user_id"]
    today = datetime.datetime.now().date()
    start = today + datetime.timedelta(days=(7 - today.weekday()))
    end = start + datetime.timedelta(days=6)
    workload = database.get_workload_next_week(user_id, start, end)
    status = round(workload / 38, 2)

    return {
        "message":"get workload success",
        "workload":status
    }