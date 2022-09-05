from django.db import models

departments = [('Cardiologist', 'Cardiologist'),
               ('Dermatologists', 'Dermatologists'),
               ('Emergency Medicine Specialists', 'Emergency Medicine Specialists'),
               ('Allergists/Immunologists', 'Allergists/Immunologists'),
               ('Anesthesiologists', 'Anesthesiologists'),
               ('Colon and Rectal Surgeons', 'Colon and Rectal Surgeons')
               ]


class User:
    def __init__(self, _id=None, _nom=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                 _profilepic=None):
        self.id = _id
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
        self.prenom = d["prenom"]
        self.mobile = d["mobile"]
        self.status = d["status"]
        self.profile_pic = d["profile_pic"]
        self.admitDate = d["admitDate"]
        self.address = d["address"]


############################
class Patient:
    def __init__(self, _user=None, _id=None, _staff=[], _symptoms=None,
                 _assignedDoctorId=None):
        self.user = _user
        self.id = _id
        self.staff = _staff
        self.symptoms = _symptoms
        self.assignedDoctorId = _assignedDoctorId

    def todict(self):
        d = {"user": self.user.todict(),
             "id": self.id,
             "staff": self.staff,
             "symptoms": self.symptoms,
             "assignedDoctorId": self.assignedDoctorId
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
        self.staff = d["staff"]
        self.symptoms = d["symptoms"]
        self.assignedDoctorId = d["assignedDoctorId"]

    def __str__(self):
        return self.user.nom + " (" + self.symptoms + ")"


#################################################################################
class Staff:
    def __init__(self, _user=None, _id=None,
                 _department=None,
                 _patients=None):
        self.user = _user
        self.id = _id
        self.department = _department
        self.patients = _patients

    def todict(self):
        d = {"user": self.user.todict(),
             "id": self.id,
             "patients": self.patients,
             "department": self.department,

             }
        return d

    def fromdict(self, d):
        user=User()
        user.fromdict(d["user"])
        self.user = user
        self.id = d["id"]
        self.department = d["department"]
        self.patients = d["patients"]

    def __str__(self):
        return self.user.nom + " (" + self.department + ")"


class Doctor(Staff):
    def __init__(self, _user=None, _id=None, _department=None, _patients=None, _specialty=None):
        super().__init__(_user, _id,  _department, _patients)
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
