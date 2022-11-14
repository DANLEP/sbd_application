from DAO.idao import IDAO
from DAO.mysql_dao import MySQLDAO
from DAO.type_dao import TypeDAO


class DAOFactory(object):
    dao: IDAO = None

    @staticmethod
    def get_dao_instance(dao_type: TypeDAO):

        if dao_type == TypeDAO.MySQL:
            if not DAOFactory.dao:
                DAOFactory.dao = MySQLDAO()

        return DAOFactory.dao
