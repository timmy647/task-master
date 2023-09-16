from datetime import datetime, timedelta
from classes import *
from register import online_user
from check_function import token_check, is_valid_email
from datainteraction import Database

def task_create(database: Database, token: str, task:dict):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    email = task.get('assigned_user')
    if type(email) != str:
        return {"message": "assigned_user should be string"}, 400
    if not is_valid_email(email):
        return {"message": "assigned_user should be email"}, 400
    if not database.is_registered_email(email):
        return {"message": "not existed user"}, 404

    user_info = database.get_userinfo_from_email(email)
    assigned_user = user_info["user_id"]
    if not assigned_user == user.get_user_id():
        if not database.is_connected_users(assigned_user, user.get_user_id()):
            return {"message": "you can only assign yourself or your connections tasks"}, 401


    title = task.get('title')
    if type(title) != str:
        return {"message": "title should be string"}, 400
    if not len(title.split(' ')) <= 20:
        return {"message": "title should not more than 20 words"}, 400

    description = task.get('description')
    if type(description) != str:
        return {"message": "description should be string"}, 400
    if not len(description.split(' ')) <= 1000:
        return {"message": "description should not more than 1,000 words"}, 400

    deadline = task.get('deadline')
    if not deadline == 'None':
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            return {"message": "deadline should be YYYY-MM-DD"}, 400
    try:
        task_estimated_time = int(task.get('task_estimated_time'))
    except:
        return {"message": "task_estimated_time should be integer"}, 400

    database.add_new_task(assigned_user, title, description, deadline, task_estimated_time)
    # update task history
    task_id = int(database.get_task_num() - 1)
    now = datetime.today()
    database.add_task_history(task_id, now, assigned_user, title, description, deadline,"Not Started", task_estimated_time)
    return {"message":"create task success"}, 200

def task_detail(database:Database, token:str, task_id:int):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    try:
        task_id = int(task_id)
    except:
        return {"message":"task_id should be integer"}, 400

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    try:
        task = database.get_task_info(task_id)
    except Exception as e:
        return {"message": "{}".format(e)}, 400

    assigned_user = task["assigned_user"]
    if not user.get_user_id()== assigned_user:
        if not database.is_connected_users(user.get_user_id(), assigned_user):
            return {"message": "not connected task master"}, 401
    email = database.get_userinfo_from_userid(assigned_user).get("user_email")
    task["assigned_user"] = email
    return {"message": "get task detail success",
            "task": task
            }, 200

def task_update(database:Database, token:str, task_id:int, task:dict):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    try:
        task_id = int(task_id)
    except:
        return {"message":"task_id should be integer"}, 400

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    email = task.get('assigned_user')
    if type(email) != str:
        return {"message": "assigned_user should be string"}, 400
    if not is_valid_email(email):
        return {"message": "assigned_user should be email"}, 400
    if not database.is_registered_email(email):
        return {"message": "not existed user"}, 404
        
    user_info = database.get_userinfo_from_email(email)
    assigned_user = user_info["user_id"]
    if not assigned_user == user.get_user_id():
        if not database.is_connected_users(assigned_user, user.get_user_id()):
            return {"message": "you can only update your or your connections' tasks"}, 401

    title = task.get('title')
    if not len(title.split(' ')) <= 20:
        return {"message": "title should not more than 20 words"}, 400

    description = task.get('description')
    if not len(description.split(' ')) <= 1000:
        return {"message": "description should not more than 1,000 words"}, 400

    deadline = task.get('deadline')
    if not deadline == 'None':
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d")
        except ValueError:
            return {"message": "deadline should be YYYY-MM-DD"}, 400

    try:
        task_estimated_time = int(task.get('task_estimated_time'))
    except:
        return {"message": "task_estimated_time should be integer"}, 400

    task_status = task.get('task_status')
    if type(task_status) != str:
        return {"message": "task_status should be string"}, 400
    # update task history
    now = datetime.today()
    database.add_task_history(task_id, now, assigned_user, title, description, deadline,task_status, task_estimated_time)
    database.update_task(task_id, assigned_user, title, description, deadline, task_status,task_estimated_time)

    return {"message": "update task success"}, 200

"""def task_delete(database:Database, token, task_id):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    #task = database.delete
    return {"message": "delete task success"}, 200"""

# def task_search(database:Database, token:str, keyvalue:dict):
#     user = token_check(token, online_user)
#     if user == None:
#         return {"message": "authorization error"}, 401

#     # check key is correct
#     for key in keyvalue.keys():
#         if not key in ['task_id', 'Title', 'Description', 'Deadline']:
#             return {"message": "property error"}, 400

#     task_id = None
#     title = None
#     description = None
#     deadline = None
#     tasks = database.search_task(task_id, title, description, deadline)
#     return {
#         "message": "search task success",
#         "task":tasks
#     }, 200


def task_list(database:Database, token:str, email:str):
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

    if user.get_user_id() != user_id:
        if not database.is_connected_users(user.get_user_id(), user_id):
            return {"message": "you should add connection first"}, 401

    task_list = database.get_all_tasks_of_user(user_id)
    for task in task_list:
        assigned_user_id = task["assigned_user"]
        task["assigned_user"] = database.get_userinfo_from_userid(assigned_user_id).get("user_email")
    task_list.reverse()
    return {"message": "get task list success",
            "task_list": task_list}, 200
        


def watch_add(database:Database, token, task_id):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    try:
        task_id = int(task_id)
    except:
        return {"message":"task_id should be integer"}, 400

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    if database.is_watching(user.get_user_id(), task_id):
        return {"message": "already watched"}, 401

    today = datetime.today()
    database.add_waching(user.get_user_id(), task_id, today)
    return {"message": "add watch success"}, 200

def watch_cancel(database:Database, token, task_id):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    try:
        task_id = int(task_id)
    except:
        return {"message": "task_id should be integer"}, 400

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    if not database.is_watching(user.get_user_id(), task_id):
        return {"message": "already not watched"}, 401

    database.unwatch_task(user.get_user_id(), task_id)
    return {"message": "cancel watch success"}, 200

def watch_list(database:Database, token, email):
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

    watching_list = database.get_watching_list(user_id)
    tasks = []
    for task in watching_list:
        task_id = task["task_id"]
        task_info = database.get_task_info(task_id)
        email = database.get_userinfo_from_userid(task_info["assigned_user"]).get("user_email")
        task_info["assigned_user"] = email
        tasks.append(task_info)

    return {
                "message":"get watching list success",
                "watching_list":tasks
            }, 200

def watch_update(database:Database, token, task_id):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    try:
        task_id = int(task_id)
    except:
        return {"message":"task_id should be integer"}, 400

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    today = datetime.today()
    database.update_last_checked_time(user.get_user_id(), task_id, today)
    return {"message": "task watching update success"}, 200


def watch_check(database:Database, token, task_id):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    try:
        task_id = int(task_id)
    except:
        return {"message": "task_id should be integer"}, 400

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    result = database.is_watching(user.get_user_id(), task_id)
    return {"message": "watch check success",
            "result":result
            }, 200


def notification(database:Database, token):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    task_notification = database.get_notification_list(user.get_user_id())

    return {
                "message":"notification success",
                "notification": task_notification
           }, 200

def task_history(database:Database, token, task_id):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    try:
        task_id = int(task_id)
    except:
        return {"message": "task_id should be integer"}, 400

    if not database.is_valid_taskid(task_id):
        return {"message": "not exist task_id"}, 404

    task_info = database.get_task_info(task_id)
    if not task_info["assigned_user"] == user.get_user_id():
        if not database.is_connected_users(task_info["assigned_user"], user.get_user_id()):
            return {"message":"you can only get your or your connections' task's history"}, 401

    history = database.get_task_histories(task_id)
    update_list = []
    keys = list(history[0].keys())
    keys.remove("updated_time")
    for i in range(1, len(history)):
        cur = history[i]
        prev = history[i - 1]
        update_item = {}
        for key in keys:
            if not cur[key] == prev[key]:
                update_item[key] = cur[key]
                if key == "assigned_user":
                    userinfo = database.get_userinfo_from_userid(update_item[key])
                    email = userinfo["user_email"]
                    update_item[key] = email
        update_item["updated_time"] = history[i].get("updated_time")
        update_list.append(update_item)



    return {
        "message":"get history success",
        "history":update_list
    }, 200


def recommendation(database: Database, token: str):
    user = token_check(token, online_user)
    if user == None:
        return {"message": "authorization error"}, 401

    connection_list = database.get_connection_list(user.get_user_id())
    workload_list = []

    today = datetime.now().date()
    start = today + timedelta(days=(7 - today.weekday()))
    end = start + timedelta(days=6)
    for user_id in connection_list:
        workload = database.get_workload_next_week(user_id, start, end)
        workload = round(workload / 38, 2)
        if workload > 0.50:
            continue

        email = database.get_userinfo_from_userid(user_id).get("user_email")
        workload_list.append({
            "email": email,
            "workload": workload
        })
    print(workload_list)
    if len(workload_list) > 0:
        workload_list = sorted(workload_list, key=lambda x: x["workload"])

    workload_list = workload_list[:20]
    return {
               "message": "get recommendation success",
               "list": workload_list
           }, 200

