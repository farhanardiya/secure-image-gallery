from flask_restx import Namespace, Resource, fields, reqparse
from flask_jwt_extended import create_access_token
from ..model.users import Users
from ..util.password_hash import check_password
from datetime import timedelta
from app.logger import logger
import traceback
from ..extensions import db

api = Namespace('login', 'Login API')

token_model = api.model(
    "Token Model", {
        "token": fields.String()
    }
)

login_response = api.model(
    "Login Response Model", {
        "code": fields.Integer(),
        "message": fields.String(),
        "errors": fields.List(fields.String()),
        "data": fields.Nested(token_model)
    }
)

params = reqparse.RequestParser()
params.add_argument('username', location='json')
params.add_argument('password', location='json')

@api.route("")
class Login(Resource):
    @api.expect(params)
    @api.marshal_with(login_response)
    def post(self):
        param_value = params.parse_args()
        username = param_value["username"]
        password = param_value["password"]
        expire_time = timedelta(hours=8)

        try:
            query = db.session.query(Users).filter(Users.username == username).first()
            db.session.close()

            if query:
                if check_password(password, query.password.replace(" ","")):
                    identity = {
                        "user_id": query.user_id
                    }

                    access_token = create_access_token(identity=identity, expires_delta=expire_time)
                    logger.info('Successful login for user: ' + username)

                    return {
                        "code": 200,
                        "message": "OK",
                        "errors": [],
                        "data": {
                            "token": access_token
                        }
                    }, 200
                else:
                    return {
                        "code": 400,
                        "message": "Bad Request",
                        "errors": ["Invalid credentials"],
                        "data": None
                    }, 400
            else:
                return {
                    "code": 400,
                    "message": "Bad Request",
                    "errors": ["Invalid credentials"],
                    "data": None
                }, 400
            
        except Exception as e:
            traceback.print_exc()
            return {
                "code": 500,
                "message": "Internal Server Error",
                "errors": ["Something went wrong"],
                "data": None
            }, 400
