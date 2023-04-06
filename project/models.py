from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_security import RoleMixin

db = SQLAlchemy()

users_roles = db.Table( 'usuario_roles',
 db.Column('userId', db.Integer, db.ForeignKey('usuario.id')),
 db.Column('roleId', db.Integer, db.ForeignKey('roles.id'))
)

class User(db.Model,UserMixin):
    __tablename__ = 'usuario'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    estatus = db.Column(db.Integer, nullable=False)
    roles= db.relationship('Role',
                           secondary= users_roles,
                           backref= db.backref('users', lazy= 'dynamic')
                           )
    
    def has_role(self, *args):
        return set(args).issubset({roles.name for roles in self.roles})

class Role (RoleMixin, db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(50))