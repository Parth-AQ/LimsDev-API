import hmac
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, get_jwt_identity
from flask_restful import Resource, reqparse
from models.user_models import UserModels
from flask_mail import Message
from mail import mail


import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class UserLogin(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument("email",
                              type=str,
                              required=True,
                              location='json',
                              help = "email is required!!")
    user_parser.add_argument("password",
                              type=str,
                              required=True,
                              location='json',
                              help = "password is required!!")

    @classmethod
    def post(cls):
        logger.info("Start*********************")
        data = cls.user_parser.parse_args()
        logger.info(f"data===========>   {data}")
        user = UserModels.find_by_email(data["email"])

        response_data = {}
        if user and hmac.compare_digest(user.password, data["password"]):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            response_data["data"] = {
                "access_token": access_token,
                "refresh_token": refresh_token
                }
            response_data["data"]["profile"] = user.json()
            del response_data["data"]["profile"]["id"]
            response_data["message"] = "User logged in Successfully"
            response_data["status"] = "success"
            return (
                response_data,
                200,
                {"Content-Type": "application/json"}
            )

        logger.info("access_token not genrated")

        response_data["message"] = "Invalid credentials"
        response_data["status"] = "Un-authorized"
        response_data["data"] = {}
        return (response_data,
                401,
                {"Content-Type": "application/json"})

class UserProfile(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = UserModels.find_by_id(user_id)
        response_data = {}
        if user:
            response_data["data"] = user.json()
            del response_data["data"]["id"]
            response_data["status"] = "success"
            return (
                response_data,
                200,
                {"Content-Type": "application/json"})
        response_data["message"] = "Data not found!!"
        response_data["status"] = "Bad Request"
        response_data["data"] = {}
        return (
            response_data,
            400,
            {"Content-Type": "application/json"})

class UpdateUserProfile(Resource):
    user_parser = reqparse.RequestParser()
    user_parser.add_argument("email",
                             type=str,
                             required=True,
                             location='json',
                             help="email is required!!")
    user_parser.add_argument("first_name",
                             type=str,
                             required=True,
                             location='json',
                             help="first_name is required!!")
    user_parser.add_argument("last_name",
                             type=str,
                             required=True,
                             location='json',
                             help="last_name is required!!")

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        user_data = UserModels.find_by_id(user_id)
        response_data = {}
        if user_data:
            data = UpdateUserProfile.user_parser.parse_args()
            response_data["data"] = {}
            try:
                user_data.email = data["email"]
                user_data.first_name = data["first_name"]
                user_data.last_name = data["last_name"]
                user_data.save_to_db()
                response_data["message"] = "Update Successfully"
                response_data["status"] = "success"
            except:
                response_data["message"] = "An error occurred updating the item"
                response_data["status"] = "Server Error"
                return (response_data,
                        500,
                        {"Content-Type": "application/json"})
        return (response_data,
                200,
                {"Content-Type": "application/json"})

class ForgetPassword(Resource):

    def get(self, email):
        is_email_valid = UserModels.find_by_email(email)
        response_data = {}
        if is_email_valid:
            try:
                token = UserModels.get_reset_token(email=email)
                msg = Message()
                msg.subject = "Test Lims Dev"
                msg.sender = "abiliquest@gmail.com"
                msg.recipients = [email]
                msg.body = f'Link'
                mail.send(msg)
                response_data["data"] = {"token": token}
                response_data["message"] = "Email varification link sent"
                response_data["status"] = "success"
                return(response_data,
                        200, {"Content-Type": "application/json"})
            except:
                response_data["data"] = {}
                response_data["message"] = "Something went wrong!!"
                response_data["status"] = "Internal Server Error"
                return {response_data,
                        500, {"Content-Type": "application/json"}}

        response_data["data"] = {}
        response_data["message"] = "Invalid Email"
        response_data["status"] = "Un-authorized"
        return (response_data,
                401, {"Content-Type": "application/json"})