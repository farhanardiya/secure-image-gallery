from flask_restx import Namespace, Resource, fields, reqparse
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from datetime import datetime
from app.logger import logger
import traceback
from ..extensions import db
from ..model.user_image import UserImage
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..util.image import validate_image, encrypt_image, decrypt_image
from ..config import ENCRYPTION_KEY

api = Namespace('image', 'Image API')

image_model = api.model(
    "Image Model", {
        "image_id": fields.String(),
        "image_name": fields.String(),
        "mime_type": fields.String(),
        "image_data": fields.String()
    }
)

get_image_response = api.model(
    "Get Images Response", {
        "code": fields.Integer(),
        "message": fields.String(),
        "errors": fields.List(fields.String()),
        "data": fields.List(fields.Nested(image_model))
    }
)

upload_image_response = api.model(
    "Upload Image Response", {
        "code": fields.Integer(),
        "message": fields.String(),
        "errors": fields.List(fields.String()),
        "data": fields.String()
    }
)

delete_image_response = api.model(
    "Delete Image Response", {
        "code": fields.Integer(),
        "message": fields.String(),
        "errors": fields.List(fields.String()),
        "data": fields.String()
    }
)

params = reqparse.RequestParser()
params.add_argument('file',type=FileStorage, location='files')

@api.route("")
class Image(Resource):
    @jwt_required(locations=["headers"])
    def get(self):
        data = []

        user_id = get_jwt_identity()["user_id"]
        try:
            query = db.session.query(UserImage).filter(UserImage.user_id == user_id).all()

            for image in query:
                image_data = decrypt_image(image.iv, image.image_enc, ENCRYPTION_KEY)

                if image_data:
                    dataset = {
                        "image_id": str(image.image_id),
                        "image_name": image.image_name,
                        "mime_type": image.mime_type,
                        "image_data": decrypt_image(image.iv, image.image_enc, ENCRYPTION_KEY)
                    }

                    data.append(dataset)
            
            return {
                "code": 200,
                "message": "OK",
                "errors": [],
                "data": data
            }, 200
        except Exception as e:
            traceback.print_exc()
            return {
                "code": 500,
                "message": "Internal Server Error",
                "errors": ["Something went wrong"],
                "data": None
            }, 500
    
    @api.expect(params)
    @jwt_required(locations=["headers"])
    def post(self):
        user_id = get_jwt_identity()["user_id"]
        param_value = params.parse_args()
        image = param_value["file"]

        # File validation
        valid, message, mime_type = validate_image(image)
        image_name = secure_filename(image.filename)

        if valid:
            # Encrypt image
            iv, image_enc = encrypt_image(image, ENCRYPTION_KEY)

            # Insert DB Entry
            created_at = int(datetime.now().timestamp())
            created_by = user_id
            updated_at = created_at
            updated_by = created_by

            entry = UserImage(user_id=user_id, image_name=image_name, mime_type=mime_type, iv=iv, image_enc=image_enc, created_at=created_at, created_by=created_by, updated_at=updated_at, updated_by=updated_by)
            db.session.add(entry)
            db.session.commit()
            db.session.close()
            
            return {
                "code": 200,
                "message": "OK",
                "errors": [],
                "data": "Image upload successful"
            }, 200
            
        else:
            return {
                "code": 400,
                "message": "Bad Request",
                "errors": [message, mime_type],
                "data": None
            }, 400

@api.route("/<string:id>")
class ImageId(Resource):
    @jwt_required(locations=["headers"])
    def delete(self, id):
        user_id = get_jwt_identity()["user_id"]

        try:
            # Check whether image is owned by user
            query = db.session.query(UserImage).filter(UserImage.user_id == user_id).filter(UserImage.image_id == id).first()
            db.session.close()

            if query:
                # Delete entry from DB
                UserImage.query.filter(UserImage.image_id == id).delete()
                db.session.commit()
                db.session.close()

                return {
                    "code": 200,
                    "message": "OK",
                    "errors": [],
                    "data": "Image successfully deleted"
                }, 200
            else:
                return {
                    "code": 404,
                    "message": "Not Found",
                    "errors": ["Image not found"],
                    "data": None
                }, 404

        except Exception as e:
            return {
                "code": 500,
                "message": "Internal Server Error",
                "errors": ["Something went wrong"],
                "data": None
            }, 500
