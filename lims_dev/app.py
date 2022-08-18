import json
# from flask_lambda import FlaskLambda #***************** FOR SERVER **********************************
from flask import Flask #**************************** FOR LOCAL ***********************************
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

from mail import mail
from db import db
from datetime import timedelta

from resources.user import (UserLogin, UserProfile,
                            UpdateUserProfile, ForgetPassword)
from resources.labs import (CreateLabs, UpdateLabs,
                            LabList, DeleteLab, LabDetail)
from models.user_models import UserModels

# app = FlaskLambda(__name__) #***************** FOR SERVER **********************************
app = Flask(__name__) #**************************** FOR LOCAL ***********************************
cors = CORS(app, allow_headers=["Content-Type"], resources={r"*": {"origins": "*"}})

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://limsdev:limsdatabase@lims-dev.cdkcr45ml0z6.ap-south-1.rds.amazonaws.com:3306/LIMS_dev'
app.config["PROPAGATE_EXCEPTIONS"] = True

# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=7200)
app.config['JWT_AUTH_USERNAME_KEY'] = 'AQ-LIMS-dev'
app.secret_key = "AQ-LIMS-dev"

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "abiliquest@gmail.com"
app.config['MAIL_PASSWORD'] = "tdzzqsnixcgaqnmt"

# app.config['CORS_HEADERS'] = 'Content-Type'

# cors = CORS(app,
#             resources={r"*": {"origins": "*"}},
#             allow_headers=["Content-Type", "Authorization", "Access-Control-Allow-Credentials", "Access-Control-Allow-Origin", "Access-Control-Allow-Methods"],
#             supports_credentials=True
#             )
api = Api(app)

db.init_app(app) #***************** FOR SERVER **********************************
mail.init_app(app)
jwt = JWTManager(app)

@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if UserModels.find_email_is_superadmin(identity): # Instead of hard-coding, you should read from a config file or a database
        return {"is_superadmin": True}
    return {"is_superadmin": False}


api.add_resource(UserLogin, "/login")
api.add_resource(UserProfile, "/profile")
api.add_resource(UpdateUserProfile, "/update_profile")
api.add_resource(ForgetPassword, "/forgetpassword/<string:email>")

api.add_resource(CreateLabs, "/createlab")
api.add_resource(UpdateLabs, "/updatelab/<int:lab_id>")
api.add_resource(LabList, "/labs")
api.add_resource(DeleteLab, "/lab/<int:lab_id>/<string:name>")
api.add_resource(LabDetail, "/lab/<int:lab_id>/<string:name>")


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
#     response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
#     return response


# **************************** FOR LOCAL ***********************************
if __name__ == "__main__":
    # db.init_app(app)
    app.run(debug=True)