from django.db import models




class User:
    def __init__(self, _email=None , _id=None, _nom=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                 _profilepic=None):
        self.id = _id
        self.email=_email
        self.nom = _nom
        self.prenom = _prenom
        self.mobile = _mobile
        self.address = _address
        self.admitDate = _admitDate
        self.status = _status
        self.profile_pic = _profilepic

    def todict(self):
        d = {"mobile": self.mobile,
             "id": self.id,
             "nom": self.nom,
             "email": self.email,
             "prenom": self.prenom,
             "address": self.address,
             "admitDate": self.admitDate,
             "status": self.status,
             "profile_pic": self.profile_pic
             }
        return d

    def fromdict(self, d):
        self.id = d["id"]
        self.nom = d["nom"]
        self.email = d["email"]
        self.prenom = d["prenom"]
        self.mobile = d["mobile"]
        self.status = d["status"]
        self.profile_pic = d["profile_pic"]
        self.admitDate = d["admitDate"]
        self.address = d["address"]


############################
class Patient:
    def __init__(self, _user=None, _id=None, _weight=None, _height=None, _age=None, _state=None,
                 _symptoms: object = None,
                 _room: object = None) -> object:
        self.user = _user
        self.age =_age
        self.id = _id
        self.weight = _weight
        self.height=_height
        self.state=_state
        self.symptoms = _symptoms
        self.room = _room

    def todict(self):
        d = {"user": self.user.todict(),
             "id": self.id,
             "room": self.room,
             "symptoms": self.symptoms,
             "state": self.state,
             "age":self.age ,
             "weight":self.weight,
             "height":self.height ,

             }
        return d

    # {'symptoms': ['fievre'], 'user': 'OaSLe32anqlIt3ty7KyA', 'id': 'ivmHEOigYDo1LgUmN2In',
    #  'staff': ['QKVlrXh5Uf9uizQGjuYD'], 'assignedDoctorId': 'CyjTIhInlmVgZuYw2zos
    #                                                         '}

    def fromdict(self, d):
        user = User()
        user.fromdict(d["user"])
        self.user = user
        self.id = d["id"]
        self.age=d["age"]
        self.room = d["room"]
        self.symptoms = d["symptoms"]
        self.state = d["state"]
        self.height = d["height"]
        self.weight= d["weight"]


    def __str__(self):
        return self.user.nom + " (" + self.symptoms + ")"


#################################################################################
class Staff:
    def __init__(self, _user=None, _id=None,
                 _department=None,
                 _rooms=None ):
        self.user = _user
        self.id = _id
        self.department = _department
        self.rooms = _rooms

    def todict(self):
        d = {"user": self.user.todict(),
             "id": self.id,
             "department": self.department,
             "rooms":self.rooms

             }
        return d

    def fromdict(self, d):
        user=User()
        user.fromdict(d["user"])
        self.user = user
        self.id = d["id"]
        self.department = d["department"]
        self.rooms=d["rooms"]

    def __str__(self):
        return self.user.nom + " (" + self.department + ")"


class Doctor(Staff):
    def __init__(self, _user=None, _id=None, _department=None,  _specialty=None , _rooms=None):
        super().__init__(_user, _id,  _department, _rooms)
        self.specialty = _specialty

    def todict(self):
        d = super().todict()
        d["specialty"] = self.specialty
        return d

    def fromdict(self, d):
        super().fromdict(d)
        self.specialty = d["specialty"]

    def __str__(self):
        return super().__str__() + "\n Specialty : " + self.specialty


class Room:
    def __init__(self, _doctor=None ,
                 _staff=None,_id=None,
                 _patients=None , _nb_beds=None , _number=None ,_department=None ):
        self.doctor=_doctor
        self.staff=_staff
        self.department=_department
        self.nbBeds=_nb_beds
        self.number=_number
        self.patients = _patients
        self.id=_id


    def todict(self):
        d = {"number": self.number,
             "id": self.id,
             "nbBeds":self.nbBeds,
             "doctor":self.doctor,
             "patients": self.patients,
             "staff": self.staff,
             "department":self.department

             }
        return d

    def fromdict(self, d):
        self.department = d["department"]
        self.doctor = d["doctor"]
        self.id = d["id"]
        self.number = d["number"]
        self.patients = d["patients"]
        self.staff = d["staff"]
        self.nbBeds=d["nbBeds"]

    def __str__(self):
        return str(self.id)+"  room number " +str(self.number)
