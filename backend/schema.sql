drop table if exists Watchings;
drop table if exists Histories;
drop table if exists Tasks;
drop table if exists Connections;
drop table if exists Connection_Requests;
drop table if exists Users;


create table Users (
    user_id integer,
    username varchar(40) NOT NULL,
    email varchar(100) NOT NULL,
    pass_encoded varchar(256) NOT NULL,
    primary key (user_id),
    unique (email)
);

create table Tasks (
    task_id integer,
    assigned_user integer,
    title varchar(40) NOT NULL,
    t_description varchar(256) NOT NULL,
    deadline date,
    task_status varchar(11) check (task_status in ('Not Started','In Progress','Blocked','Completed')),
    task_estimated_time integer NOT NULL,
    primary key (task_id),
    foreign key (assigned_user) references Users(user_id)
);

create table Connection_Requests (
    sender_id integer references Users(user_id),
    receiver_id integer references Users(user_id),
    request_status varchar(8) check (request_status in ('Waiting','Accepted','Rejected')),
    primary key (sender_id,receiver_id)
);

create table Connections (
    sender_id integer references Users(user_id),
    receiver_id integer references Users(user_id),
    starting_date date NOT NULL,
    primary key (sender_id,receiver_id)
);

create table Histories (
    task_id integer references Tasks(task_id),
    updated_time timestamp without time zone NOT NULL,
    assigned_user integer,
    title varchar(40) NOT NULL,
    t_description varchar(256) NOT NULL,
    deadline date,
    task_status varchar(11) check (task_status in ('Not Started','In Progress','Blocked','Completed')),
    task_estimated_time integer NOT NULL,
    primary key (task_id,updated_time),
    foreign key (assigned_user) references Users(user_id)
);

create table Watchings (
    user_id integer references Users(user_id),
    task_id integer references Tasks(task_id),
    last_checked_time timestamp without time zone NOT NULL,
    primary key (user_id,task_id)
);
