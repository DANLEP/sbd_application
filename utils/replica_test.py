import time
from pprint import pprint
import random

from pymongo import WriteConcern
from pymongo.read_concern import ReadConcern

from DAO.mongo_dao import MongoDAO
from utils.score_test import generate_users

mongo = MongoDAO(conn_str='mongodb://localhost:27001,localhost:27002,localhost:27003/?replicaSet=myReplSet')


def insert_test(users):
    mongo_save_start = time.time()
    for user in users:
        mongo.save_user_dict(user, w_concern=WriteConcern(w=0, j=False))
    mongo_save_end = time.time()

    return {
        "test": "insert",
        "amount": len(users),
        "mongo_db": round(mongo_save_end - mongo_save_start, 2),
        "mongo_db_c": mongo_save_end - mongo_save_start,
    }

def select_test(rec, test_email):
    mongo_start = time.time()
    mongo.get_user_dict(test_email, r_concern=ReadConcern(level="local"))
    mongo_end = time.time()

    return {
        "test": "select",
        "amount": rec,
        "mongo_db": round(mongo_end - mongo_start, 2),
        "mongo_db_c": mongo_end - mongo_start,
    }

if __name__ == '__main__':
    mongo.delete_all_users()
    users = generate_users(10_000)

    insert_res = insert_test(users)

    pprint(insert_res)

    test_email = random.choice(users)['email']
    select_res = select_test(10_000, test_email)
    pprint(select_res)
