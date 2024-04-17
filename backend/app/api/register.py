from flask_restx import Namespace, Resource, fields, reqparse
from ..model.users import Users
from ..util.password_hash import hash_password
from ..util.password_req import validate_password
from ..util.username_req import validate_username
from datetime import datetime
from app.logger import logger
import traceback
from ..extensions import db

api = Namespace('register', 'Register API')

register_response = api.model(
    "Register Response Model",
    {
        "code": fields.Integer(),
        "message": fields.String(),
        "errors": fields.List(fields.String()),
        "data": fields.String()
    }
)

params = reqparse.RequestParser()
params.add_argument('username', location='json')
params.add_argument('password', location='json')

@api.route("")
class Register(Resource):
    @api.expect(params)
    @api.marshal_with(register_response)
    def post(self):
        params_value = params.parse_args()
        username = params_value["username"]
        password = params_value["password"]

        # Check username requirements
        if validate_username(username):
            try:
                check_user = db.session.query(Users.username).filter(Users.username == username).first()

                if check_user:
                    # User already exists
                    return {
                        "code": 400,
                        "message": "Bad Request",
                        "errors": ["User already exists"],
                        "data": None
                    }, 400
                else:
                    # User does not exist yet
                    # Check password requirements
                    if validate_password(password):
                        password_hash = hash_password(password)

                        created_at = int(datetime.now().timestamp())
                        created_by = username
                        updated_at = created_at
                        updated_by = created_by

                        new_user = Users(username=username, password=password_hash, is_active=True, created_at=created_at, created_by=created_by, updated_at=updated_at, updated_by=updated_by)
                        db.session.add(new_user)
                        db.session.commit()
                        db.session.close()
                        logger.info('Success register user: ' + username + " created at: " + str(created_at) + " created by: " + created_by)

                        return {
                            "code": 200,
                            "message": "OK",
                            "errors": [],
                            "data": "Successfully created new user!"
                        }, 200
                    else:
                        return {
                            "code": 400,
                            "message": "Bad Request",
                            "errors": ["Password does not meet requirements"],
                            "data": None
                        }, 400

            except Exception as e:
                traceback.print_exc()
                return {
                    "code": 500,
                    "message": "Internal Server Error",
                    "errors": ["Something went wrong"],
                    "data": None
                }, 500
        else:
            return {
                "code": 400,
                "message": "Bad Request",
                "errors": ["Username does not meet requirements"],
                "data": None
            }, 400
