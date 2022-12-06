# models.py

from flask_login import UserMixin
from . import db , app
# import db, app
import uuid
from sqlalchemy.dialects.postgresql import UUID
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    active = db.Column(db.Integer, nullable=False, default=0)

class Code(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    token = db.Column(UUID(as_uuid=True), default=uuid.uuid4)
    active = db.Column(db.Integer, nullable=False, default=0)
    
    def get_cu(self):
        return self.token

admin = Admin(app)
admin.add_view(ModelView(Code, db.session))
admin.add_view(ModelView(User, db.session))