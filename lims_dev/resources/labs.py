from flask_jwt_extended import (jwt_required,
                                get_jwt,
                                get_jwt_identity)
from flask_restful import Resource, reqparse
from models.lab_models import LabModel
import urllib.parse

_parser = reqparse.RequestParser()
_parser_dict = {"name": True,
               "full_name": True,
               "address1": True,
               "address2": False,
               "phone_no": False,
               "fax": False,
               "email": True,
               "website": False,
               "CLIA": False,
               "director_name": False,
               "logo": False,
               "approved_by": False,
               "supervisor_name": False}
for name, required in _parser_dict.items():
    _parser.add_argument(name,
                        type=str,
                        required=required,
                        location='json',
                        help=f"{name} is required!!")

class CreateLabs(Resource):


    @jwt_required()
    def post(self):
        data = _parser.parse_args()
        if LabModel.find_by_labname(data["name"]):
            return ({
                       "message": "An lab with name '{}' already exists".format(data["name"]),
                        "status": "Bad Request",
                        "data": {}
                    },
                    400,
                    {"Content-Type": "application/json"}
            )

        lab = LabModel(**data)
        try:
            lab.save_to_db()
        except:
             return ({
                     "message": "An error occurred creating lab",
                     "status": "Internal Server Error",
                     "data": {}
                 }, 500, {"Content-Type": "application/json"})

        return ({
                "message": "Data Created Successfully",
                "status": "success"
            }, 201, {"Content-Type": "application/json"})

class UpdateLabs(Resource):

    @jwt_required()
    def put(self, lab_id):
        data = _parser.parse_args()
        lab_name = LabModel.find_by_labname_and_id(lab_id, data["name"])
        if lab_name:
            try:
                lab_name.full_name = data["full_name"]
                lab_name.address_1 = data["address1"]
                lab_name.address_2 = data["address2"]
                lab_name.phone_no = data["phone_no"]
                lab_name.fax = data["fax"]
                lab_name.email = data["email"]
                lab_name.website = data["website"]
                lab_name.CLIA = data["CLIA"]
                lab_name.director_name = data["director_name"]
                lab_name.logo = data["logo"]
                lab_name.approved_by = data["approved_by"]
                lab_name.supervisor_name = data["supervisor_name"]

                lab_name.save_to_db()
                return ({
                            "message": "Lab Updated Successfully",
                            "status": "success",
                            "data": {}
                        }, 201,
                        {"Content-Type": "application/json"})
            except:
                return ({
                            "message": "An error occurred updating the lab",
                            "status": "Bad Request",
                            "data": {}
                        }, 500, {"Content-Type": "application/json"})
        else:
            return ({
                    "message": "Lab Does Not Exists!!!",
                    "status": "Bad Request","data":{}}, 400,
                    {"Content-Type": "application/json"})


class LabList(Resource):
    @jwt_required()
    def get(self):
        labs = LabModel.get_all_labs()
        return ({
                    "status": "success",
                    "data": labs
                },
                200, {"Content-Type": "application/json"})


class DeleteLab(Resource):
    # parser = reqparse.RequestParser()
    # parser.add_argument("name",
    #                     type=str,
    #                     required=True,
    #                     location='json',
    #                     help=f"Lab name is required!!")

    @jwt_required()
    def delete(self, lab_id, name):
        claims = get_jwt()
        if not claims["is_superadmin"]:
            return ({
                        "message": "SuperAdmin privilege required.",
                        "status": "Un-authorized",
                        "data": {}
                     },
                    401, {"Content-Type": "application/json"})
        name = urllib.parse.unquote_plus(name)
        # data = self.parser.parse_args()
        lab = LabModel.find_by_labname_and_id(lab_id, name)
        if lab:
            lab.delete_from_db()
        return ({"message": "Lab deleted",
                 "status": "success", "data": {}},
                200,  {"Content-Type": "application/json"})

class LabDetail(Resource):

    @jwt_required()
    def get(self, lab_id, name):

        claims = get_jwt()
        if not claims["is_superadmin"]:
            return ({
                        "message": "SuperAdmin privilege required.",
                        "status": "Un-authorized",
                        "data": {}
                    },
                    401, {"Content-Type": "application/json"})
        name = urllib.parse.unquote_plus(name)
        lab = LabModel.find_by_labname_and_id(lab_id, name)
        if lab:
            return ({"data": lab.json(),
                    "status": "success"},
                    200, {"Content-Type": "application/json"})
        return ({"message": "no data available",
                 "status": "Not Found", "data":{}},
                404, {"Content-Type": "application/json"})
