from flask_sqlalchemy import SQLAlchemy
import sqlalchemy as sa


class Database:
    def __init__(self,app):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:''@localhost/arsistant'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.db = SQLAlchemy(app)

    def getDb(self):
        return self.db
         
# class User(Model):

#     username = sa.Column(sa.String(30),primary_key=True)
#     password = sa.Column(sa.String(30))
#     azienda = sa.Column(sa.String(20))
#     email = sa.Column(sa.String(30),unique = True)
#     admin = sa.Column(sa.Boolean)

#     def __init__(self,username,password,azienda,email,admin):
#         self.username = username
#         self.password = password
#         self.azienda = azienda
#         self.email = email
#         self.admin = admin


# class Images(Model):

#     id = sa.Column(sa.Integer,primary_key=True)
#     name = sa.Column(sa.String(30))
#     model = sa.Column(sa.String(20))
#     type = sa.Column(sa.String(20))
#     floor = sa.Column(sa.String(20))
#     azienda = sa.Column(sa.String(20))
#     # path = db.Column(sa.String(20))
#     base64 = sa.Column(sa.String(64))
    

#     def __init__(self,name,model,type,floor,base64,azienda):
#         self.name = name
#         self.model = model
#         self.type = type
#         self.floor = floor
#         self.base64 = base64
#         self.azienda = azienda

# class Azienda(Model):

#     id = sa.Column(sa.Integer,primary_key=True)
#     name = sa.Column(sa.String(30))
#     code = sa.Column(sa.String(30))
#     floors = sa.Column(sa.String(2))

#     def __init__(self,name):
#         self.name = name
