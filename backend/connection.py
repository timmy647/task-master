from check_function import *
from datainteraction import Database
from register import online_user

def connection_request(database: Database, token:str, email:str):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    if type(email) != str:
        return {"message": "email should be string"}, 400
    if not is_valid_email(email):
        return {"message": "email should be email"}, 400
    if not database.is_registered_email(email):
        return {"message": "not exist user"}, 404

    if user.get_email() == email:
        return {"message":"cannot connect with yourself"}, 400

    sender = user.get_user_id()
    receiver_info = database.get_userinfo_from_email(email)
    receiver = receiver_info["user_id"]
    if database.is_connected_users(sender, receiver):
        return {"message": "already connected"}, 400

    if database.is_exist_request(sender, receiver):
        status = database.get_connection_request_status(sender, receiver)
        if status == "Waiting":
            return {"message": "waiting receiver confirm"}, 200
        if status == "Rejected":
            database.update_request_status(sender, receiver, "Waiting")
            return {"message": "connection request send success"}, 200

    database.add_connection_request(sender, receiver)

    return {"message": "connection request send success"}, 200

def connection_receive(database: Database, token:str, email:str, status:str):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    if type(email) != str:
        return {"message": "email should be string"}, 400
    if not is_valid_email(email):
        return {"message": "email should be email"}, 400
    if not database.is_registered_email(email):
        return {"message": "not exist user"}, 404

    user_id = database.get_userinfo_from_email(email).get("user_id")
    sender = user_id
    receiver = user.get_user_id()

    if not database.is_exist_request(sender, receiver):
        return {"message": "connection request not exist"}, 404

    if database.is_connected_users(sender, receiver):
        return {"message": "already connected"}, 200

    if status == 'Accepted':
        database.add_connection(sender, receiver)

    database.update_request_status(sender, receiver, status)
    if database.is_exist_request(receiver, sender):
        database.update_request_status(receiver, sender, status)
    message = "connection " + status + " success"
    return {"message": message}, 200

def connection_request_list(database:Database, token:str):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    request_list = database.get_connection_request_list(user.get_user_id())
    request_info = []

    for user_id in request_list:
        sender = database.get_userinfo_from_userid(user_id)
        request_info.append(
            {
                "name": sender["user_name"],
                "email": sender["user_email"]
            })
    return {
        "message": "get connection request list success",
        "connection_request_list": request_info
    }, 200

def connection_list(database:Database, token:str, email):
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
    user_id = user.get_user_id()

    if not user_info["user_id"] == user_id:
        user_id = user_info["user_id"]
        if not database.is_connected_users(user.get_user_id(), user_id):
            return {"message": "you should add connection first"}, 401

    connect_list = database.get_connection_list(user_id)
    connect_info = []

    for user_id in connect_list:
        user_info = database.get_userinfo_from_userid(user_id)
        connect_info.append({
            "name": user_info["user_name"],
            "email": user_info["user_email"]
        })
    return {
        "message": "get connection list success",
        "connection_list": connect_info
    }, 200