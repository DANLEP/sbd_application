from DAO.dao_factory import DAOFactory
from DAO.type_dao import TypeDAO

dao = DAOFactory.get_dao_instance(TypeDAO.MONGO)
