from api.shared.infraestructure.utils import get_db_engine

db_engine = get_db_engine(
    user='db_user',
    password='1Passw0rd2345',
    host='tipsy_db',
    port='5432',
    db_name='tipsy_db')
