import sqlite3 
from database_utils import economy_queries

def connect():
    return sqlite3.connect("database_utils/database.db")

def create_members_table(connection):
    with connection:
        connection.execute(economy_queries.CREATE_MEMBERS_TABLE)

def create_ranks_table(connection):
    with connection:
        connection.execute(economy_queries.CREATE_RANKS_TABLE)

def add_member(connection, userid, name, money, rank):
    with connection:
        connection.execute(economy_queries.INSERT_MEMBER, (userid, name, money, rank))

def add_rank(connection, name, minsalary, maxsalary, required, position):
    with connection:
        connection.execute(economy_queries.INSERT_RANK, (name, minsalary, maxsalary, required, position))

def add_member_money(connection, userid, money):
    money += get_member_by_userid(connection, userid)[0][3]
    with connection:
        connection.execute(economy_queries.UPDATE_MEMBER_MONEY, (money, userid))

def get_all_members(connection):
    with connection:
        return connection.execute(economy_queries.GET_ALL_MEMBERS).fetchall()

def get_all_members_by_networth(connection):
    with connection:
        return connection.execute(economy_queries.GET_ALL_MEMBERS_BY_NETWORTH).fetchall()

def get_all_ranks(connection):
    with connection:
        return connection.execute(economy_queries.GET_ALL_RANKS).fetchall()

def get_member_by_userid(connection, userid):
    with connection:
        return connection.execute(economy_queries.GET_MEMBER_BY_USERID, (userid,)).fetchall()

def get_rank_by_name(connection, name):
    with connection:
        return connection.execute(economy_queries.GET_RANK_BY_NAME, (name,)).fetchall()

def get_rank_by_position(connection, position):
    with connection:
        return connection.execute(economy_queries.GET_RANK_BY_POSITION, (position,)).fetchall()

def delete_member_by_userid(connection, userid):
    with connection:
        connection.execute(economy_queries.DELETE_MEMBER, (userid,))

def delete_rank_by_name(connection, name):
    with connection:
        connection.execute(economy_queries.DELETE_RANK, (name,))