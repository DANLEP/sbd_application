import time
from pprint import pprint
import random

from DAO.mongo_dao import MongoDAO
from DAO.mysql_dao import MySQLDAO
from utils.fake_user import generate_user

mongo = MongoDAO()
mysql = MySQLDAO()


def generate_users(amount):
    print("Start generating users")
    users = []
    for _ in range(amount):
        users.append(generate_user().dict())
    print("Users generated")
    return users


def insert_test(users):
    mongo_save_start = time.time()
    for user in users:
        mongo.save_user_dict(user)
    mongo_save_end = time.time()
    print("s")
    mysql_save_start = time.time()
    for user in users:
        mysql.save_user_dict(user)
    mysql_save_end = time.time()

    return {
        "test": "insert",
        "amount": len(users),
        "mongo_db": round(mongo_save_end - mongo_save_start, 2),
        "mysql_db": round(mysql_save_end - mysql_save_start, 2),
        "mongo_db_c": mongo_save_end - mongo_save_start,
        "mysql_db_c": mysql_save_end - mysql_save_start
    }


def select_test(rec, test_email):
    mongo_start = time.time()
    mongo.get_user_dict(test_email)
    mongo_end = time.time()

    mysql_start = time.time()
    mysql.get_user_dict(test_email)
    mysql_end = time.time()

    return {
        "test": "select",
        "amount": rec,
        "mongo_db": round(mongo_end - mongo_start, 2),
        "mysql_db": round(mysql_end - mysql_start, 2),
        "mongo_db_c": mongo_end - mongo_start,
        "mysql_db_c": mysql_end - mysql_start
    }


if __name__ == '__main__':
    # users = generate_users(500_000)
    users = generate_users(10)
    # test_rec = [100, 1000, 10_000, 50_000, 100_000, 500_000]
    test_rec = [10]

    for test in test_rec:
        mysql.delete_all_users()
        mongo.delete_all_users()

        insert_res = insert_test(users[:test])
        pprint(insert_res)

        test_email = random.choice(users[:test])['email']
        select_res = select_test(test, test_email)
        pprint(select_res)
