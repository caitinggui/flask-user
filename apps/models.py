# coding: utf-8

from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app as app
from . import db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired


class Permission(object):
    """权限值不是越大就越高，只是用二进制标记而已
    通过Role绑定Permission，然后User再绑定Role来完成权限控制。
    如果要精确到某个文章，再通过具体文章和用户的所属关系判断"""
    ADMIN = 1     # 0b000000000000001
    DOWNLOAD = 2  # 0b000000000000010


class Role(db.Model):
    """在设置admin user时，需要把所有的权限值加起来赋给permisssions"""
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions = db.Column(db.BigInteger, default=0)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insertRoles():
        roles = {
            "User": [Permission.DOWNLOAD],
            "Admin": [Permission.ADMIN]
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if not role:
                role = Role(name=r)
            role.resetPermission()
            for perm in roles[r]:
                role.addPermission(perm)
            db.session.add(role)
        db.session.commit()

    def resetPermission(self):
        self.permissions = 0

    def hasPermission(self, perm):
        return self.permissions & perm == perm

    def addPermission(self, perm):
        if not self.hasPermission(perm):
            self.permissions += perm

    def removePermission(self, perm):
        if not self.hasPermission(perm):
            self.permissions -= perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(128))
    avatar = db.Column(db.String(255))

    def __init__(self, **kwargs):
        """注册的用户默认无role，且部分路由仅需login_required"""
        super(User, self).__init__(**kwargs)

    def can(self, perm):
        """admin默认拥有所有的权限"""
        if self.role:
            return self.role.hasPermission(perm) or self.isAdmin()
        return False

    def isAdmin(self):
        if self.role:
            return self.role.hasPermission(Permission.ADMIN)
        return False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def info(self):
        info = {
            "email": self.email,
            "username": self.username,
            "avatar": self.avatar
        }
        return info

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except Exception:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username
