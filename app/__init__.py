"""Setup at app startup"""
import os
import sqlalchemy
from flask import Flask
from yaml import load, Loader



def init_connection_engine():
    """ initialize database setup
    Takes in os variables from environment if on GCP
    Reads in local variables that will be ignored in public repository.
    Returns:
        pool -- a connection to GCP MySQL
    """


    # detect env local or gcp
    if os.environ.get('GAE_ENV') != 'standard':
        try:
            variables = load(open("app.yaml"), Loader=Loader)
        except OSError as e:
            print("Make sure you have the app.yaml file setup")
            os.exit()

        env_variables = variables['env_variables']
        for var in env_variables:
            os.environ[var] = env_variables[var]

    pool = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=os.environ.get('MYSQL_USER'),
            password=os.environ.get('MYSQL_PASSWORD'),
            database=os.environ.get('MYSQL_DB'),
            host=os.environ.get('MYSQL_HOST')
        )
    )

    return pool


def init_connection_local_engine():
    return sqlalchemy.create_engine('mysql+pymysql://root:MySql&Ykx_114428@localhost/team_97')  

app = Flask(__name__)
# db = init_connection_engine()
db = init_connection_local_engine()

# conn = db.connect()
# query = 'SELECT listing_id, price, D.description, D.room_type, D.property_type, D.bedrooms, D.beds, D.picture_url \
#         FROM (SELECT listing_id, ROUND(AVG(price),2) price FROM calendar WHERE date >= "{}" AND date < "{}" AND available = 1 \
#             GROUP BY listing_id HAVING COUNT(listing_id) >= datediff( "{}" , "{}") ) AS available \
#         NATURAL JOIN (SELECT * FROM description WHERE beds+1 >= {}) AS D;'.format("2021-04-19", "2021-04-21", "2021-04-21", "2021-04-19", 4)
# df = conn.execute(query).fetchall()
# i = 0
# for elem in df:  
#     print(float(elem[1]))
#     if i==0 :
#         break

# To prevent from using a blueprint, we use a cyclic import
# This also means that we need to place this import here
# pylint: disable=cyclic-import, wrong-import-position
from app import routes
