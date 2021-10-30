from flask import Flask
from database import db
from sqlalchemy_utils import create_database, database_exists
from routes.routes import blue_print
from flask_jwt_extended import JWTManager
import datetime
import os

app = Flask(__name__)

#Base de datos
db_user = os.environ.get('DB_USUARIO')
db_password = os.environ.get('DB_CLAVE')
db_host = os.environ.get('DB_HOST')
db_name = os.environ.get('DB_NOMBRE')

DB_URL = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=12)

#JWT
jwt = JWTManager(app)

#Inicializar SQLAlchemy
db.init_app(app)

#Instacioacion de rutas
app.register_blueprint(blue_print)

with app.app_context():
    if not database_exists(DB_URL):
        create_database(DB_URL)
    db.create_all()

@app.route('/',methods=['GET'])
def inicio():
    return "<h1>Flask API</h1>"

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True,port=5000)
