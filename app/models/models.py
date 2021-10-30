from database import db

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20) , nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    firstname = db.Column(db.String(70), nullable=False)
    lastname = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(125), nullable=True)

    def __init__(self,username,password,firstname,lastname,email):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

class Movies(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    moviename = db.Column(db.String(100),nullable=False,unique=True)
    premiere = db.Column(db.String(20),nullable=False)
    director = db.Column(db.String(50),nullable=False)
    starring = db.Column(db.String(250),nullable=False)
    genre = db.Column(db.String(50),nullable=False)
    resume = db.Column(db.String(250),nullable=False)

    def __init__(self, moviename, premiere, director, starring, genre, resume):
        self.moviename = moviename
        self.premiere = premiere
        self.director = director
        self.starring = starring
        self.genre = genre
        self.resume = resume
