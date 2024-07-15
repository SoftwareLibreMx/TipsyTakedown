from sqlalchemy import create_engine


def get_db_engine(user, password, host, port, db_name):
    return create_engine(
        f'postgresql://{user}:{password}@{host}:{port}/{db_name}')
