from flask_sqlalchemy import SQLAlchemy
import urllib.parse
import config

# creat object
con1 = config.mysqlDB_creds()

db = SQLAlchemy()
class mysqlDB_conn:
    def __init__(self,app):
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{con1.DB_USERNAME}:{urllib.parse.quote_plus(con1.DB_PASSWORD)}@{con1.DB_HOST}/{con1.DB_NAME}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
    
