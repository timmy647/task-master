from encode import *

class User:
    def __init__(self, username, email, password, user_id):
        self.username = username
        self.email = email
        self.password = password_encode(password)
        self.user_id = user_id
        self.token = generate_token(self.user_id)

    def put_username(self, username):
        self.username = username

    def put_email(self, email):
        self.email = email

    def put_password(self, password):
        self.password = password_encode(password)

    def put_token(self, token):
        self.token = token

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def get_user_id(self):
        return self.user_id

    def get_token(self):
        return self.token

'''class Task:
    def __init__(self, task_id, assigned_user, title, description, deadline, status, estimated_time):
        self.id = task_id,
        self.assigned_user = assigned_user,
        self.title = title,
        self.description = description,
        self.deadline = deadline
        self.status = status
        self.estimated_time = estimated_time

    def put_id(self, task_id):
        self.id = task_id

    def put_assigned_user(self, user):
        self.assigned_user = user

    def put_title(self, title):
        self.title = title

    def put_description(self, description):
        self.description = description

    def put_deadline(self, deadline):
        self.deadline = deadline

    def put_status(self, status):
        self.status = status

    def put_estimated_time(self, estimated_time):
        self.estimated_time = estimated_time

    def get_id(self):
        return self.id

    def get_assigned_user(self):
        return self.assigned_user

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_deadline(self):
        return self.deadline

    def get_status(self):
        return self.status

    def get_estimated_time(self):
        return self.estimated_time'''



if __name__ == '__main__':
    pass

