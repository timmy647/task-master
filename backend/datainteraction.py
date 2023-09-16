import psycopg2
import datetime
from error import *
from classes import User


class Database:

    def __init__(self):
        # try to connect the default database
        try:
            self.db = psycopg2.connect(
                database="postgres",
                user="postgres",
                password="admin",
                host="localhost",
                port="5433"
            )
        except psycopg2.Error as err:
            print("DB error: ", err)

    def close_database(self):
        '''
        close the database
        '''
        self.db.close()

    # ------------------------------- IS -----------------------------------
    def is_registered_email(self, email: str):
        '''
        check whether email is active
        :param email:
        :return: Boolean
        '''

        query = """
        select *
        from Users u
        where u.email = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [email])
            result = cursor.fetchall()
        email_num = len(result)

        # email has been registed
        if email_num > 0:
            return True
        else:
            return False

    def is_valid_userid(self, user_id: int):
        '''
        check user id whether exist
        :param user_id:
        :return: bool
        '''
        if type(user_id) != int:
            return False
        pattern = str(user_id)

        query = """
        select u.user_id
        from Users u
        where u.user_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [pattern])
            result = cursor.fetchall()
        id_num = len(result)

        # user_id exists return true
        if id_num > 0:
            return True
        else:
            return False

    def is_correct_password(self, email: str, password: str):
        '''
        check email and password whether match in database
        :param email:
        :param password:
        :return: bool
        '''

        query = """
        select *
        from Users u
        where u.email = %s and u.pass_encoded = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [email, password])
            result = cursor.fetchall()
        match_account = len(result)

        # account with correct email and password
        if match_account > 0:
            return True
        else:
            return False
    def is_exist_request(self, id1: int, id2: int):
        '''
        check connection request between id1 and id2
        :param id1:
        :param id2:
        :return: bool
        '''
        query = """
                select *
                from Connection_Requests cr
                where cr.sender_id = %s and cr.receiver_id = %s;
                """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(id1), str(id2)])
            result = cursor.fetchall()
        if len(result) > 0:
            return True
        else:
            return False
    def is_connected_users(self, id1: int, id2: int):
        '''
        check id1 and id2 whether connected
        :param id1:
        :param id2:
        :return: bool
        '''

        query = """
        select *
        from Connections c
        where c.sender_id = %s and c.receiver_id = %s;
        """
        # sender: id1, receiver: id2
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(id1), str(id2)])
            result1 = cursor.fetchall()
            sender_id1 = len(result1)

            # sender: id2, receiver: id1
            cursor.execute(query, [str(id2), str(id1)])
            result2 = cursor.fetchall()
            sender_id2 = len(result2)

        # have connection record
        if sender_id1 > 0 or sender_id2 > 0:
            return True
        else:
            return False

    def is_valid_taskid(self, task_id: int):
        '''
        check task_id whether exist
        :param task_id:
        :return: bool
        '''

        if type(task_id) != int:
            return False

        pattern = str(task_id)

        query = """
        select t.task_id
        from Tasks t
        where t.task_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [pattern])
            result = cursor.fetchall()
        id_num = len(result)

        # user_id exists return true
        if id_num > 0:
            return True
        else:
            return False

    def is_valid_check_task(self, task_id: int, user_id: int):
        '''
        check is this task can be checked by the user (assigned user is the user_id or conncected users)
        :param task_id:
        :param user_id:
        :param assigned_user:
        :return: bool
        :exeption: AccessError :if no such task_id or no assigned_user of this task
        '''

        query = """
        select t.assigned_user
        from Tasks t
        where t.task_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(task_id)])
            result = cursor.fetchall()
        if len(result) > 0:
            assigned_user = result[0][0]
            # assigned_user is self return True
            if assigned_user == user_id:
                return True
            else:
                # check assigned user is connected user or not
                result = self.is_connected_users(user_id, assigned_user)
                return result
        else:
            raise AccessError(
                f'no such task task_id = {task_id} or no assigned_user of this task')

    def is_watching(self, user_id: int, task_id: int):
        '''
        check is the task watched by the user
        :param user_id:
        :param task_id:
        :return: bool
        '''

        query = """
        select w.user_id
        from Watchings w
        where w.user_id = %s and w.task_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(user_id), str(task_id)])
            result = cursor.fetchall()
        watching = len(result)

        # user_id exists return true
        if watching > 0:
            return True
        else:
            return False

    # ------------------------------- ADD -----------------------------------
    def add_new_user_user(self, user: User):
        '''
        write a new user into database
        :param user: User
        :return: {}
        '''
        userdata = [(str(user.get_user_id()), user.get_username(),
                     user.get_email(), user.get_password())]
        insert_query = "insert into users values (%s, %s, %s, %s)"
        with self.db.cursor() as cursor:
            cursor.execute(insert_query, userdata)

        # Commit the change
        self.db.commit()

        return {}

    def add_new_user(self, username: str, email: str, pass_encoded: str):
        '''
        write a new user into database
        :param username: str
        :param email: str
        :param pass_encoded: str
        :return: {}
        '''

        # generate new userID, new userID = number of user in database (start from 1)
        user_id = self.get_user_num()

        userdata = (str(user_id), username, email, pass_encoded)
        insert_query = "insert into users values (%s, %s, %s, %s)"
        with self.db.cursor() as cursor:
            cursor.execute(insert_query, userdata)

        # Commit the change
        self.db.commit()

        return {}

    def add_connection_request(self, sender: int, receiver: int):
        '''
        create a connection request
        :param sender:
        :param receiver:
        :return: {}
        '''
        connect_request_data = (sender, receiver, 'Waiting')
        insert_query = "insert into Connection_Requests values (%s, %s, %s)"
        with self.db.cursor() as cursor:
            cursor.execute(insert_query, connect_request_data)

        # Commit the change
        self.db.commit()

        return {}

    def add_connection(self, sender: int, receiver: int):
        '''
        create a connection
        :param sender:
        :param receiver:
        :return: {}
        '''
        
        # connect_data = (sender, receiver, datetime.datetime.now(datetime.timezone.utc))
        connect_data = (sender, receiver, datetime.datetime.now())
        insert_query = "insert into Connections values (%s, %s, %s)"
        with self.db.cursor() as cursor:
            cursor.execute(insert_query, connect_data)

        # Commit the change
        self.db.commit()

        return {}

    def add_new_task(self, assigned_user: int, title: str, description: str, deadline: datetime.date,
                     task_estimated_time: int):
        '''
        create a new task
        :param user_id:
        :param title:
        :param description:
        :param task_estimated_time:
        :param deadline (option):
        :return: {}
        '''

        # generate new task_id, new task_id = number of tasks in database (start from 0)
        task_id = self.get_task_num()

        with self.db.cursor() as cursor:
            if not deadline == 'None':
                task_data = [str(task_id), str(assigned_user), title, description, str(deadline), 'Not Started',
                            str(task_estimated_time)]
                insert_query = "insert into Tasks values (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, task_data)

            else:
                task_data = [
                    str(task_id), str(assigned_user), title, description, 'Not Started', str(task_estimated_time)]
                insert_query = "insert into Tasks (task_id, assigned_user, title, t_description, task_status, task_estimated_time) values (%s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, task_data)

        # Commit the change
        self.db.commit()

        return {}

    # log for histories

    def add_task_history(self, task_id: int, updated_time: datetime.datetime, assigned_user: int, title: str, description: str, deadline: datetime.date,
                     task_status: str, task_estimated_time: int):
        '''
        create a new task
        :param task_id:
        :param updated_time: from frontend
        :param user_id:
        :param title:
        :param description:
        :param task_estimated_time:
        :param deadline (option):
        :return: {}
        '''

        with self.db.cursor() as cursor:
            if not deadline == 'None':
                log_data = [str(task_id), str(updated_time), str(assigned_user), title, description, str(deadline), task_status,
                            str(task_estimated_time)]
                insert_query = "insert into Histories values (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, log_data)

            else:
                log_data = [
                    str(task_id), str(updated_time), str(assigned_user), title, description, task_status, str(task_estimated_time)]
                insert_query = "insert into Histories (task_id, updated_time, assigned_user, title, t_description, task_status, task_estimated_time) values (%s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(insert_query, log_data)

        # Commit the change
        self.db.commit()

        return {}

    def add_waching(self, user_id: int, task_id: int, last_checked_time: datetime.datetime):
        '''
        create a watching relationship
        :param user_id:
        :param task_id:
        :param last_checked_time:
        :return: {}
        '''
        watching_data = [str(user_id), str(task_id), str(last_checked_time)]
        insert_query = "insert into Watchings values (%s, %s, %s)"
        with self.db.cursor() as cursor:
            cursor.execute(insert_query, watching_data)

        # Commit the change
        self.db.commit()

        return {}

    # ------------------------------- GET -----------------------------------

    def get_user_num(self):
        '''
        :return: Int: number of user in database
        '''
        query = """
        select u.user_id
        from Users u;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        user_num = len(result)

        return user_num

    def get_task_num(self):
        '''
        :return: Int: number of task in database
        '''
        query = """
        select t.task_id
        from Tasks t;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()

        tasl_num = len(result)

        return tasl_num

    def get_userinfo_from_userid(self, user_id: int):
        '''
        use user_id to get information from database
        :param user_id:
        :return: {"user_id": user_id, "user_name": user_name, "user_email": user_email}
        :exeption: AccessError :if no such userID
        '''

        query = """
        select u.username, u.email
        from Users u
        where u.user_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(user_id)])
            result = cursor.fetchall()
        match_account = len(result)

        # account with correct email and password
        if match_account > 0:
            # get user info from result
            user_name = result[0][0]
            user_email = result[0][1]

            return {"user_id": user_id, "user_name": user_name, "user_email": user_email}
        else:
            raise AccessError(f"no such user from use_id : {user_id}")

    def get_userinfo_from_email(self, email: str):
        '''
        use email to get information from database
        :param email:
        :return: {"user_id": user_id, "user_name": user_name, "user_email": user_email}
        :exeption: AccessError :if no such userID
        '''

        query = """
        select *
        from Users u
        where u.email = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [email])
            result = cursor.fetchall()
        match_account = len(result)

        # account with correct email and password
        if match_account > 0:
            # get user info from result
            user_id = result[0][0]
            user_name = result[0][1]
            user_email = result[0][2]

            return {"user_id": user_id, "user_name": user_name, "user_email": user_email}
        else:
            raise AccessError(f"no such user from email : {email}")

    def get_connection_request_status(self, sender: int, receiver: int):
        '''
        get the connection status
        :param sender:
        :param receiver:
        :return: status: str
        '''

        query = """
        select cr.request_status
        from Connection_Requests cr
        where cr.sender_id = %s and cr.receiver_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(sender), str(receiver)])
            result = cursor.fetchall()

        # have connection record
        if len(result) > 0:
            return str(result[0][0])

        else:
            raise AccessError(
                f'no such connection_Request of sender_id = {sender} and receiver_id = {receiver}')

    def get_connection_request_list(self, user_id:int):
        '''
        get all received connections request of a user
        :param user_id:
        :return: connection_list: [user_id]
        '''
        connection_request_list = []

        query = """
                select cr.sender_id
                from Connection_Requests cr
                where cr.receiver_id = %s and cr.request_status = %s;
                """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(user_id), "Waiting"])
            result_request = cursor.fetchall()

        for i in result_request:
            uid = i[0]
            connection_request_list.append(uid)

        connection_request_list = set(connection_request_list)
        connection_request_list = list(connection_request_list)
        return connection_request_list

    def get_connection_list(self, user_id: int):
        '''
        get all connections of a user
        :param user_id:
        :return: connection_list: [user_id]
        '''

        connection_list = []

        # sender: user_id, all connections (receiver)

        query = """
        select c.receiver_id
        from Connections c
        where c.sender_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, str(user_id))
            result_receiver = cursor.fetchall()

        for i in result_receiver:
            connection_list.append(i[0])

        # receiver: user_id, all connections (sender)
        query = """
        select c.sender_id
        from Connections c
        where c.receiver_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, str(user_id))
            result_sender = cursor.fetchall()

        for i in result_sender:
            connection_list.append(i[0])

        # prevent repeating connection
        connection_list = set(connection_list)
        connection_list = list(connection_list)
        return connection_list

    def get_watching_list(self, user_id: int):
        '''
        get all watching of a user
        :param user_id:
        :param task_id:
        :param last_checked_time:
        :return: [{task_id, last_checked_time}]
        '''

        watching = []

        query = """
        select w.task_id, w.last_checked_time
        from Watchings w
        where w.user_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(user_id)])
            result = cursor.fetchall()

        for i in result:
            task_id = i[0]
            last_checked_time = i[1]
            watching.append(
                {"task_id": task_id, "last_checked_time": last_checked_time})

        # print watching
        return watching

    def get_task_info(self, task_id: int):
        '''
        get task information from task_id
        :param task_id:
        :return: {"task_id": task_id, "assigned_user": assigned_user, "title": title, "description": description, "deadline": deadline, "task_status": task_status, "task_estimated_time": task_estimated_time}
        :exeption: AccessError :if no such task_id
        '''
        if type(task_id) != int:
            raise AccessError(f"task_id should be int, not {type(task_id)}")
        query = """
        select *
        from Tasks t
        where t.task_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(task_id)])
            result = cursor.fetchall()
        match_task = len(result)

        if match_task > 0:
            # get task info from result
            task_id = int(result[0][0])
            assigned_user = int(result[0][1])
            title = result[0][2]
            description = result[0][3]
            deadline = result[0][4]
            task_status = result[0][5]
            task_estimated_time = result[0][6]

            #if deadline != 'None':
                # need to check if type change has error
                #deadline = datetime.date(deadline)

            return {"task_id": task_id, "assigned_user": assigned_user, "title": title, "description": description,
                    "deadline": deadline, "task_status": task_status, "task_estimated_time": task_estimated_time}
        else:
            raise AccessError(f"no such task from task_id : {task_id}")

    def get_task_histories(self, task_id: int):
        '''
        get task histories from task_id
        :param task_id:
        :return: [{"task_id": task_id, "updated_time": updated_time, "assigned_user": assigned_user, "title": title, "description": description,
                    "deadline": deadline, "task_status": task_status, "task_estimated_time": task_estimated_time}]
        :exeption: AccessError :if no such task_id
        '''
        histories = []

        query = """
        select *
        from Histories h
        where h.task_id = %s
        order by h.updated_time;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(task_id)])
            result = cursor.fetchall()
        match_task = len(result)

        if match_task > 0:
            # get task histories from result
            for row in result:
                task_id = int(row[0])
                # need to check if timestamp type correct

                updated_time = row[1]
                assigned_user = row[2]
                title = row[3]
                description = row[4]
                deadline = row[5]
                task_status = row[6]
                task_estimated_time = row[7]

                # if deadline != 'None':
                #    deadline = datetime.date(deadline)  # need to check if type change has error

                history = {"task_id": task_id, "updated_time": updated_time, "assigned_user": assigned_user, "title": title, "description": description,
                    "deadline": deadline, "task_status": task_status, "task_estimated_time": task_estimated_time}
                histories.append(history)

            return histories
        else:
            return histories
            
    def get_all_tasks_of_user(self, user_id: int):
        '''
        get all task information of a user from user_id
        :param user_id:
        :return: [{"task_id": task_id, "assigned_user": assigned_user, "title": title, "description": description, "deadline": deadline, "task_status": task_status, "task_estimated_time": task_estimated_time}]
        :exeption: AccessError :if no such user_id
        '''

        tasks = []

        if type(user_id) != int:
            raise AccessError(f"user_id should be int, not {type(user_id)}")
        
        query = """
        select *
        from Tasks t
        where t.assigned_user = %s
        order by t.task_id;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(user_id)])
            result = cursor.fetchall()
            match_task = len(result)
        if match_task > 0:

            tasks = self.build_task_dict(result)
            
            return tasks
        else:
            return tasks

    
    def get_notification_list(self, user_id: int):
        '''
        get a list of all watched task that need to be notificated of a user from user_id
        :param user_id:
        :return: [{"task_id": task_id, "title": title}]
        :exeption: AccessError :if no such user_id
        '''

        notifications = []

        if type(user_id) != int:
            raise AccessError(f"user_id should be int, not {type(user_id)}")
        
        query = """
        select distinct h.task_id, h.title
        from Histories h join Watchings w on (h.task_id = w.task_id)
        where w.user_id = %s and h.updated_time > w.last_checked_time;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(user_id)])
            result = cursor.fetchall()
            match_history = len(result)
        if match_history > 0:
            # get task histories from result
            for row in result:
                task_id = int(row[0])
                title = row[1]
                task = {"task_id": task_id, "title": title}
                notifications.append(task)

            return notifications
        else:
            return notifications
    
    def get_workload_next_week(self, user_id: int, start_date: datetime.date, end_date: datetime.date):
        '''
        get estimated workload in next week of a user from user_id
        :param user_id:
        :param start_date:
        :param end_date:
        :return: int
        :exeption: AccessError :if no such user_id
        :exeption: InputError :if start_date > end_date
        '''

        if type(user_id) != int:
            raise AccessError(f"user_id should be int, not {type(user_id)}")
        
        if start_date > end_date:
            raise InputError(f"start_date: {start_date} is later than end_date: {end_date}")
        

        
        query = """
        select t.task_id, t.task_estimated_time
        from Tasks t
        where t.assigned_user = %s and deadline >= %s and deadline <= %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(query, [str(user_id), str(start_date), str(end_date)])
            result = cursor.fetchall()
            match_task = len(result)
        
        total_time = 0

        if match_task > 0:
            # get task histories from result
            for row in result:
                task_time = row[1]
                total_time = total_time + task_time
                
            return total_time
        else:
            return total_time


    # ------------------------------- UPDATE -----------------------------------
    def update_task(self, task_id: int, assigned_user: int, title: str, description: str, deadline: datetime.date,
                    task_status: str, task_estimated_time: int):
        '''
        update a task from task_id
        :param task_id:
        :param assigned_user:
        :param title:
        :param description:
        :param deadline:
        :param task_status:
        :param task_estimated_time:
        :return: {}
        '''
        with self.db.cursor() as cursor:
            if deadline != 'None':
                query = """
                update tasks
                set assigned_user = %s, title = %s, t_description = %s, deadline = %s, task_status = %s, task_estimated_time = %s
                where task_id = %s;
                """
                cursor.execute(query, [str(assigned_user), title, description, str(deadline), task_status,
                                        str(task_estimated_time), str(task_id)])

            else:
                query = """
                update tasks
                set assigned_user = %s, title = %s, t_description = %s, task_status = %s, task_estimated_time = %s
                where task_id = %s;
                """
                cursor.execute(query, [str(assigned_user), title, description, task_status, str(task_estimated_time),
                                        str(task_id)])

        # Commit the change
        self.db.commit()

        return {}

    def update_request_status(self, sender_id: int, receiver_id: int, request_status: str):
        '''
        update request_status of a Connection_Request from sender_id and receiver_id
        :param sender_id:
        :param receiver_id:
        :param request_status:
        :return: {}
        '''

        query = """
        update Connection_Requests
        set request_status = %s
        where sender_id = %s and receiver_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(
                query, [request_status, str(sender_id), str(receiver_id)])

        # Commit the change
        self.db.commit()

        return {}

    def update_last_checked_time(self, user_id: int, task_id: int, last_checked_time: datetime.datetime):
        '''
        update last_checked_time of a task in Watchings from user_id and task_id
        :param user_id:
        :param task_id:
        :param last_checked_time:
        :return: {}
        '''

        query = """
        update Watchings
        set last_checked_time = %s
        where user_id = %s and task_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(
                query, [str(last_checked_time), str(user_id), str(task_id)])

        # Commit the change
        self.db.commit()

        return {}

    # ------------------------------ UNWATCH -------------------------------------
    
    def unwatch_task(self, user_id, task_id):
        '''
        unwatch a task from task_id of a user from user_id
        :param user_id:
        :param task_id:
        :return: {}
        '''
        
        query = """
        delete from Watchings
        where user_id = %s and task_id = %s;
        """
        with self.db.cursor() as cursor:
            cursor.execute(
                query, [str(user_id), str(task_id)])

        # Commit the change
        self.db.commit()

        return {}

    
    
    # # ------------------------------ SEARCH -------------------------------------
    # def search_task(self, task_id: int, title: str, description: str, deadline: datetime.date):
    #     '''
    #     search task from any combination of task_id, title (task name), description and deadline
    #     :param task_id:
    #     :param title:
    #     :param description:
    #     :param deadline:
    #     :return: [{"task_id": task_id, "assigned_user": assigned_user, "title": title, "description": description, "deadline": deadline, "task_status": task_status, "task_estimated_time": task_estimated_time}]
    #     '''

    #     set_task_id = set()
    #     set_title = set()
    #     set_description = set()
    #     set_deadline = set()
    #     results = []

    #     if task_id != None:
    #         query_task_id = """
    #         select *
    #         from Tasks t
    #         where t.task_id = %s;
    #         """
    #         self.cur.execute(query_task_id, str(task_id))
    #         result_task_id = self.cur.fetchall()
    #         set_task_id = set(self.build_task_dict(result_task_id))

    #     if title != None:
    #         query_title = """
    #         select *
    #         from Tasks t
    #         where t.title = %s;
    #         """
    #         self.cur.execute(query_title, title)
    #         result_title = self.cur.fetchall()
    #         set_title = set(self.build_task_dict(result_title))

    #     if description != None:
    #         query_description = """
    #         select *
    #         from Tasks t
    #         where t.t_description = %s;
    #         """
    #         self.cur.execute(query_description, description)
    #         result_description = self.cur.fetchall()
    #         set_description = set(self.build_task_dict(result_description))

    #     if deadline != 'None':
    #         query_deadline = """
    #         select *
    #         from Tasks t
    #         where t.deadline = %s;
    #         """
    #         self.cur.execute(query_deadline, deadline)
    #         result_deadline = self.cur.fetchall()
    #         set_deadline = set(self.build_task_dict(result_deadline))

    #     results = list(set_task_id.union(set_title.union(set_description.union(set_deadline))))
    #     return results

    # helper function for search_task()
    def build_task_dict(self, result_list: list):
        tasks = []
        result_len = len(result_list)
        if result_len > 0:
            for t in result_list:
                task_id = int(t[0])
                assigned_user = int(t[1])
                title = t[2]
                description = t[3]
                deadline = t[4]
                task_status = t[5]
                task_estimated_time = t[6]


               # if deadline != 'None':
               #     deadline = datetime.date(deadline)  # need to check if type change has error


                task = {"task_id": task_id, "assigned_user": assigned_user, "title": title, "description": description,
                        "deadline": deadline, "task_status": task_status, "task_estimated_time": task_estimated_time}
                tasks.append(task)
            return tasks
        

    


if __name__ == '__main__':
    pass
