from db import db
import datetime

class LabModel(db.Model):
    __tablename__ = 'labs'

    id = db.Column(db.Integer, autoincrement=True)
    name = db.Column(db.String(80), primary_key=True)
    full_name = db.Column(db.String(80))
    address_1 = db.Column(db.String(80))
    address_2 = db.Column(db.String(80))
    phone_no = db.Column(db.String(12))
    fax = db.Column(db.String(80))
    website = db.Column(db.String(80))
    CLIA = db.Column(db.String(80))
    director_name = db.Column(db.String(80))
    logo = db.Column(db.String(80))
    supervisor_name = db.Column(db.String(80))
    approved_by = db.Column(db.String(80))
    email = db.Column(db.String(80))
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, name, full_name, address1, address2, phone_no,
                 fax, email, website, CLIA, director_name, logo,
                 approved_by, supervisor_name
                ):
        self.name = name
        self.full_name = full_name
        self.address_1 = address1
        self.address_2 = address2
        self.phone_no = phone_no
        self.fax = fax
        self.website = website
        self.CLIA = CLIA
        self.director_name = director_name
        self.logo = logo
        self.supervisor_name = supervisor_name
        self.approved_by = approved_by
        self.email = email

    def json(self):
        return {"id": self.id,
                "name": self.name,
                "full_name": self.full_name,
                "address1": self.address_1,
                "address2": self.address_2,
                "phone_no": self.phone_no,
                "fax": self.fax,
                "CLIA": self.CLIA,
                "director_name": self.director_name,
                "log": self.logo,
                "supervisor_name": self.supervisor_name,
                "approved_by": self.approved_by,
                "email": self.email,
                "website": self.website,
                "created_at": self.created_at.strftime("%Y/%m/%d %H:%M:%S")
                }

    @classmethod
    def find_by_labname(cls, lab_name):
        return cls.query.filter_by(name=lab_name).first() # SELECT * FROM items WHERE name=name LIMIT 1

    @classmethod
    def find_by_labname_and_id(cls, lab_id, name):
        return cls.query.filter_by(id=lab_id, name=name).first()

    def save_to_db(self): # It can handle update and insert into the database
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_labs(cls):
        return [x.json() for x in cls.query.order_by(cls.created_at.desc()).all()]
