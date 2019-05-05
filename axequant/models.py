from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from axequant import db, login_manager
from flask_login import UserMixin
from mongoengine import DateTimeField
from bson import ObjectId


@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()


class User(db.Document, UserMixin):
    username = db.StringField(max_length=20, unique=True, null=False)
    email = db.StringField(max_length=120, unique=True, null=False)
    image_file = db.StringField(max_length=20, null=False, default='default.jpg')
    password = db.StringField(max_length=60, null=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': str(self.id)}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = ObjectId(s.loads(token)['user_id'])
        except:
            return None
        return User.objects.get(id=user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Document):
    title = db.StringField(max_length=100, null=False)
    date_posted = DateTimeField(null=False, default=datetime.utcnow)
    content = db.StringField(null=False)
    author = db.ReferenceField(User, reverse_delete_rule=2)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
