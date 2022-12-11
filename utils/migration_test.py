from DAO.mongo_dao import MongoDAO
from DAO.mysql_dao import MySQLDAO

mongo = MongoDAO()
mysql = MySQLDAO()


def mysql_to_mongo():
    mongo.drop_db()
    data = mysql.export_data()
    mongo.import_data(data)


def mongo_to_mysql():
    mysql.drop_db()
    data = mongo.export_data()
    mysql.import_data(data)


def main():
    # mysql_data = mysql.export_data()
    # mongo_data = mongo.export_data()
    #
    # mysql.import_data(mongo_data)
    # mongo.import_data(mysql_data)

    mysql_to_mongo()
    mongo_to_mysql()


if __name__ == '__main__':
    main()
