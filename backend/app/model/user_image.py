from ..extensions import db
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserImage(db.Model):
    __tablename__ = 'user_image'
    __table_args__ = {'schema': 'public'}
    
    image_id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID())
    image_name = db.Column(db.String(255))
    mime_type = db.Column(db.String(100))
    image_enc = db.Column(db.LargeBinary())
    iv = db.Column(db.LargeBinary())

    created_at = db.Column(BIGINT())
    created_by = db.Column(db.String(255))
    updated_at = db.Column(BIGINT())
    updated_by = db.Column(db.String(255))
    
    def __repr__(self):
        return self.image_id
