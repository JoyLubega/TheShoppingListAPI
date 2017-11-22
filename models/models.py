from datetime import datetime
from api import db
from werkzeug.security import generate_password_hash, \
    check_password_hash
from sqlalchemy import UniqueConstraint


class UserModel(db.Model):
    """
    User Database model
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    #token  = db.Column(db.String, nullable=False, unique=True)
    shoppinglists = db.relationship(
        'ShoppinglistModel', backref='user', lazy='dynamic', cascade='delete')

    def __init__(self, email, password, name=None):
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)

    @staticmethod
    def check_password(pw_hash, password):
        """ 
        Validates password        
        :param pw_hash: 
        :param password: 
        """
        return check_password_hash(pw_hash, password)

    def save(self):
        """
        Save User to DB        
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """Updates user"""
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Users"""
        return UserModal.query.all()

    def delete(self):
        """Delete User"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<User: {}>".format(self.name)

    # def encode_auth_token(user_id):
    #     """
    #     Generates the Auth Token
    #     :return: string
    #     """
    #     try:
    #         payload = {
    #             'exp': datetime.datetime.utcnow() +
    #             datetime.timedelta(days=90),
    #             'iat': datetime.datetime.utcnow(),
    #             'sub': user_id
    #         }
    #         return jwt.encode(
    #             payload,
    #             app.config.get('SECRET_KEY'),
    #             algorithm='HS256'
    #         )
    #     except Exception as e:
    #         return e

    # @staticmethod
    # def decode_auth_token(auth_token):
    #     """
    #     Decodes the auth token
    #     :param auth_token:
    #     :return: integer|string
    #     """
    #     try:
    #         payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
    #         return payload['sub']
    #     except jwt.ExpiredSignatureError:
    #         response = jsonify({
    #             'Expired': 'Signature expired. Please log in again.'
    #         })
    #         response.status_code = 401
    #         return response

    #     except jwt.InvalidTokenError:
    #         response = jsonify({
    #             'Invalid': 'Invalid token. Please log in again.'
    #         })
    #         response.status_code = 401
    #         return response


class ShoppinglistModel(db.Model):
    """
    Shoppinglist database Modae
    """
    __tablename__ = 'shoppinglists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    desc = db.Column(db.String(100))
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __table_args__ = (db.UniqueConstraint(
        'user_id', 'name', name='unq_b_name'),)

    def __init__(self, name, desc, user_id):
        self.name = name
        self.desc = desc
        self.user_id = user_id

    def save(self):
        """
        Save shoppinglist to DB
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def update():
        """Updates shoppinglist"""
        db.session.commit()


    @staticmethod
    def get_all():
        """Get all Shoppinglists"""
        ShoppinglistModel.query.all()

    def delete(self):
        """Delete Shoppinglist"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Shoppinglist: {}>".format(self.name)


class ItemModel(db.Model):
    """
    Item Database Model
    """
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(5), default=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow())
    shoppinglist_id = db.Column(db.Integer, db.ForeignKey('shoppinglists.id'))
    __table_args__ = (db.UniqueConstraint(
        'shoppinglist_id', 'name', name='unq_i_name'),)

    def __init__(self, name, shoppinglist_id):
        self.name = name
        self.shoppinglist_id = shoppinglist_id

    def save(self):
        """
        Save Item to DB
        """
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        """Get all Items"""
        ItemModel.query.all()

    def delete(self):
        """Delete Item"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self) -> str:
        return "<Item: {}>".format(self.name)
