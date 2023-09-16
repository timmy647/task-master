from flask import Flask, request
from register import *
from connection import *
from task import *
from json import dumps
from datainteraction import Database
from marshmallow import Schema, fields, ValidationError
from flask_cors import CORS

database = Database()

app = Flask(__name__)
CORS(app)

@app.route('/welcome', methods=['GET'])
def welcome():
    return 'welcome to task master!'

@app.route('/clear')
def clear():
    database.clear()

class RegisterSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)

@app.route('/auth/register', methods=['POST'])
def server_register():
    info = request.get_json()
    try:
        RegisterSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    email = info.get('email')
    password = info.get('password')
    name = info.get('name')
    message = register(database, email, password, name)
    return message

class LoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)

@app.route('/auth/login', methods=['POST'])
def server_login():
    info = request.get_json()
    try:
        LoginSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    email = info.get('email')
    password = info.get('password')
    message = login(database, email, password)
    return message

@app.route('/auth/logout', methods=['POST'])
def server_logout():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    message = logout(token)
    return message

@app.route('/profile', methods=['GET'])
def server_profile():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    email = request.args.get('email')
    try:
        email = str(email)
    except ValueError:
        return dumps({"message": "email should be string"}), 400
    message = profile(database, token, email)
    return message

@app.route('/profile/search', methods=['GET'])
def server_search_profile():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    email = request.args.get('email')
    message = search_profile(database, token, email)
    return message

@app.route('/workload',methods=['GET'])
def server_workload():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    email = request.args.get('email')
    message = workload(database, token, email)
    return message

class ConnectionRequestSchema(Schema):
    email = fields.Str(required=True)

@app.route('/connection/request', methods=['POST'])
def server_connection_request():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    info = request.get_json()
    try:
        ConnectionRequestSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    email= info.get('email')
    message = connection_request(database, token, email)
    return message

class ConnectionReceiveSchema(Schema):
    email = fields.Str(required=True)
    status = fields.Str(required=True)

@app.route('/connection/receive', methods=['POST'])
def server_connection_receive():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401

    info = request.get_json()
    try:
        ConnectionReceiveSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    email = info.get('email')
    status = info.get('status')
    message = connection_receive(database, token, email, status)
    return message

@app.route('/connection/list', methods=['GET'])
def server_connection_list():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401

    email = request.args.get('email')
    message = connection_list(database, token, email)
    return message

@app.route('/connection/request/list', methods=['GET'])
def server_connection_request_list():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    message = connection_request_list(database, token)
    return message


class TaskCreateSchema(Schema):
    task = fields.Dict(required=True)

@app.route('/task/create', methods=['POST'])
def server_task_create():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    info = request.get_json()
    try:
        TaskCreateSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    task = info.get('task')
    message = task_create(database, token, task)
    return message

# task_id is included in parameters
@app.route('/task/detail', methods=['GET'])
def server_task_detail():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    task_id = request.args.get('task_id')
    message = task_detail(database, token, task_id)
    return message

class TaskUpdateSchema(Schema):
    task_id = fields.Int(required=True)
    task = fields.Dict(required=True)

@app.route('/task/update', methods=['PUT'])
def server_task_update():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    info = request.get_json()
    try:
        TaskUpdateSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    task_id = info.get('task_id')
    task = info.get('task')
    message = task_update(database, token, task_id, task)
    return message

@app.route('/task/list', methods=['GET'])
def server_task_list():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401

    email = request.args.get('email')
    message = task_list(database, token, email)
    return message


# @app.route('/task/search', methods=['GET'])
# def server_task_search():
#     info = request.get_json()
#     token = info['token']
#     key = request.args.get('key')
#     value = request.args.get('value')
#     keyvalue = (key,value)
#     message = task_search(database, token, keyvalue)
#     return message
    
@app.route('/task/history', methods=['GET'])
def server_task_history():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    task_id = request.args.get('task_id')
    message = task_history(database, token, task_id)
    return message

@app.route('/notification', methods=['GET'])
def server_notification():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    message = notification(database, token)
    return message


class WatchAddSchema(Schema):
    task_id = fields.Int(required=True)

@app.route('/watch/add', methods=['POST'])
def server_watch_add():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    info = request.get_json()
    try:
        WatchAddSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    task_id = info.get('task_id')
    message = watch_add(database, token, task_id)
    return message

class CancelAddSchema(Schema):
    task_id = fields.Int(required=True)

@app.route('/watch/cancel', methods=['POST'])
def server_watch_cancel():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    info = request.get_json()
    try:
        CancelAddSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    task_id = info.get('task_id')
    message = watch_cancel(database, token, task_id)
    return message


@app.route('/watch/list', methods=['GET'])
def server_watch_list():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401

    email = request.args.get('email')
    message = watch_list(database, token, email)
    return message

@app.route('/watch/check', methods=['GET'])
def server_watch_check():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401

    task_id = request.args.get('task_id')
    message = watch_check(database, token, task_id)
    return message

class TaskHistoryUpdateSchema(Schema):
    task_id = fields.Int(required=True)

@app.route('/watch/update', methods=['PUT'])
def server_task_history_update():
    info = request.get_json()
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401
    try:
        TaskHistoryUpdateSchema().load(info)
    except ValidationError as err:
        return dumps(err.messages), 400
    task_id = info['task_id']
    message = watch_update(database, token, task_id)
    return message

@app.route('/recommendation', methods=['GET'])
def server_recommendation():
    token = request.headers.get('token')
    if token == None:
        return dumps({"message": "authorization error"}), 401

    message = recommendation(database, token)
    return message


if __name__ == '__main__':
    app.run(debug=True)
    database.close_database()
