from DAO.schemas.user import User, UserReg
from faker import Faker

fake = Faker()


def generate_user():

    return UserReg(
        email=fake.email(),
        password="$2b$12$IzwrnK/G/9N54o75iY0zTej/2Rxh5ptXnuC3I5uq4THpvqrpGKKAu",
        telegram_username="@"+fake.user_name()
    )
