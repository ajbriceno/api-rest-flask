from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.models import Users, Movies
from schema.schemas import movie_schema, movies_schema
from database import db
import bcrypt

blue_print = Blueprint('app',__name__)

#Ruta de inicio
@blue_print.route('/',methods=['GET'])
def inicio():
    return jsonify(respuesta="Rest API con Python, Flask y MySQL")

#Ruta de Registro de uSUARIO
@blue_print.route('/auth/registrar',methods=['POST'])
def registrar_usuario():
    try:
        #Obtener Usuario ID
        username = request.json.get('username')
        #Obtener password
        password = request.json.get('password')

        firstname = request.json.get('firstname')
        lastname = request.json.get('lastname')
        email = request.json.get('email')

        if not username:
            return jsonify(respuesta='Campo Usuario invalido'), 400
        if not password:
            return jsonify(respuesta='Campo Password invalido'), 400

        UserExist = Users.query.filter_by(username=username).first()

        if UserExist:
            return jsonify(respuesta='Usuario ya existe'), 400

        #Se encripta el password
        EncriptPass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        UserNew = Users(username, EncriptPass, firstname, lastname, email)
        db.session.add(UserNew)
        db.session.commit()

        return jsonify(respuesta='Usuario creado existosamente'), 201

    except Exception:
        return jsonify(respuesta='Error en peticion'), 500


#Ruta de Inicio de Sesion
@blue_print.route('/auth/login',methods=['POST'])
def login():
    try:
        #Obtener Usuario
        username = request.json.get('username')
        #Obtener password
        password = request.json.get('password')

        if not username:
            return jsonify(respuesta='Campo Usuario invalido')
        if not password:
            return jsonify(respuesta='Campo Password invalido')

        UserExist = Users.query.filter_by(username=username).first()

        if not UserExist:
            return jsonify(respuesta='Usuario no existe'), 400

        ValidPass = bcrypt.checkpw(password.encode('utf-8'), UserExist.password.encode('utf-8'))

        if ValidPass:
            access_token = create_access_token(identity=username)
            return jsonify(access_token = access_token), 200
        return jsonify(respuesta='Usuario o Password invalido'), 404
    except Exception:
        return jsonify(respuesta='Error de Login'), 500

""" RUTAS PROTEGIDAS PARA JWT"""

# Ruta - Crear Pelicula
@blue_print.route('/api/movies', methods=['POST'])
def create_movie():
    try:
        moviename = request.json['moviename']
        premiere =  request.json['premiere']
        director = request.json['director']
        starring = request.json['starring']
        genre = request.json['genre']
        resume = request.json['resume']

        Movie_New = Movies(moviename, premiere, director, starring, genre, resume)
        db.session.add(Movie_New)
        db.session.commit()
        return jsonify(respuesta='Pelicula ha sido guardada existosamente'), 201
    except Exception as e:
        return jsonify(respuesta = 'Error de peticion: ' + str(e)), 500

# Ruta - Obtener Peliculas
@blue_print.route('/api/movies', methods=['GET'])
@jwt_required()
def get_movies():
    try:
        movies = Movies.query.all()
        respuesta = movies_schema.dump(movies)
        return movies_schema.jsonify(respuesta), 200
    except Exception as e:
        return jsonify(respuesta = 'Error de peticion: ' + str(e)), 500

# Ruta - Obtener Pelicula por ID
@blue_print.route('/api/movies/<int:id>', methods=['GET'])
@jwt_required()
def get_movie_by_id(id):
    try:
        movie = Movies.query.get(id)
        return movie_schema.jsonify(movie), 200
    except Exception as e:
        return jsonify(respuesta = 'Error de peticion: ' + str(e)), 500

# Ruta - Actualizar Pelicula
@blue_print.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    try:
        movie = Movies.query.get(id)
        if not movie:
            return jsonify(respuesta='Pelicula no existente'), 404
        movie.moviename = request.json['moviename']
        movie.premiere =  request.json['premiere']
        movie.director = request.json['director']
        movie.starring = request.json['starring']
        movie.genre = request.json['genre']
        movie.resume = request.json['resume']
        db.session.commit()
        return jsonify(respuesta='Pelicula ha sido actualizada existosamente'), 200
    except Exception as e:
        return jsonify(respuesta = 'Error de peticion: ' + str(e)), 500

# Ruta - Eliminar Pelicula por ID
@blue_print.route('/api/movies/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_movie_by_id(id):
    try:
        delMovie = Movies.query.get(id)
        if not delMovie:
            return jsonify(respuesta='Pelicula no existente'),404
        db.session.delete(delMovie)
        db.session.commit()
        return jsonify(respuesta='Pelicula ha sido eliminada existosamente'), 200
    except Exception as e:
        return jsonify(respuesta = 'Error de peticion: ' + str(e)), 500