import os
import pyodbc

basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave123'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir, 'app.db' )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    server = '02LAB108PC25\SQLDEVELOPER'
    database = 'db_ecolink'
    username = 'sa'
    password = 'sa'
    cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server +
    ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password
    )

