from ..extensions import db
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Users(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'public'}
    
    user_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(72))
    is_active = db.Column(db.Boolean())

    created_at = db.Column(BIGINT())
    created_by = db.Column(db.String(255))
    updated_at = db.Column(BIGINT())
    updated_by = db.Column(db.String(255))
    
    def __repr__(self):
        return self.username
