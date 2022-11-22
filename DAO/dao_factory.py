from DAO.idao import IDAO
from DAO.mongo_dao import MongoDAO
from DAO.mysql_dao import MySQLDAO
from DAO.type_dao import TypeDAO


class DAOFactory:
    __dao: IDAO = None

    @staticmethod
    def get_dao_instance(dao_type: TypeDAO):
        if not DAOFactory.__dao:
            DAOFactory(dao_type)
        return DAOFactory.__dao

    def __init__(self, dao_type: TypeDAO):
        if DAOFactory.__dao:
            raise Exception("Singleton object already created!")
        else:
            if dao_type == TypeDAO.MySQL:
                DAOFactory.__dao = MySQLDAO()
            if dao_type == TypeDAO.MONGO:
                DAOFactory.__dao = MongoDAO()
