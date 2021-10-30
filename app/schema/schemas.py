from flask_marshmallow import Marshmallow

ma = Marshmallow()

#Esquema de Usuarios

class UsersSchema(ma.Schema):
    class Meta:
        fields = ('id','username','password','firstname','lastname','email')

#Esquema de Peliculas
class MoviesSchema(ma.Schema):
    class Meta:
        fields = ('id','moviename','premiere','director','starring','genre','resume')

movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)
