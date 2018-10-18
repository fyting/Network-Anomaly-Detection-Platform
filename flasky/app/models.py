from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Config(db.Model):
    __tablename__ = 'config'
    key = db.Column(db.String(64), primary_key=True)
    value = db.Column(db.String(64))



class Netflow(db.Model):

    __tablename__ = 'netflow'
    id = db.Column(db.Integer, primary_key=True)

    f1 = db.Column(db.Float)
    f2 = db.Column(db.String(16))
    f3 = db.Column(db.String(16))
    f4 = db.Column(db.String(16))
    f5 = db.Column(db.Float)
    f6 = db.Column(db.Float)
    f7 = db.Column(db.Float)
    f8 = db.Column(db.Float)
    f9 = db.Column(db.Float)

    f23 = db.Column(db.Float)
    f24 = db.Column(db.Float)
    f25 = db.Column(db.Float)
    f26 = db.Column(db.Float)
    f27 = db.Column(db.Float)
    f28 = db.Column(db.Float)
    f29 = db.Column(db.Float)
    f30 = db.Column(db.Float)
    f31 = db.Column(db.Float)

    f32 = db.Column(db.Float)
    f33 = db.Column(db.Float)
    f34 = db.Column(db.Float)
    f35 = db.Column(db.Float)
    f36 = db.Column(db.Float)
    f37 = db.Column(db.Float)
    f38 = db.Column(db.Float)
    f39 = db.Column(db.Float)
    f40 = db.Column(db.Float)
    f41 = db.Column(db.Float)

    fromIP = db.Column(db.String(32))
    fromPort = db.Column(db.Integer)

    toIP = db.Column(db.String(32))
    toPort = db.Column(db.Integer)

    timestamp = db.Column(db.DateTime())

    evalue = db.Column(db.Float)
    error = db.Column(db.Boolean)


class Sysinfo(db.Model):

    __tablename__ = 'sysinfo'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    mem_free = db.Column(db.Integer)
    mem_used = db.Column(db.Float)
    net_reci = db.Column(db.Float)
    net_send = db.Column(db.Float)
    process = db.Column(db.Integer)
    cpu_used = db.Column(db.Float)
    disk_writ = db.Column(db.Float)
    disk_read = db.Column(db.Float)