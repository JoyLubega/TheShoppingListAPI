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




class ShoppinglistModel(db.Model):
    """
    Shoppinglist database Model
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

# db.create_all()
# db.session.commit()
