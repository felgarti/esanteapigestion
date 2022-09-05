from . import firebaseConfig
from . import models
from .firebaseConfig import *
from .models import *


def create_user( _nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None):
    doc_ref = db.collection(u'users').document()
    user=User(doc_ref.id ,_nom, _prenom ,_mobile, _address, _status,_admitDate, _profilepic)
    doc_ref.set(user.todict())
    print("\nUser created succesfully ! user id : "+ doc_ref.id)
    return user

def get_user(id):
    doc = db.collection(u'users').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return

    user=User()
    user.fromdict(doc.to_dict())
    return user

# @firestore.transactional
def edit_user(user):
    doc = db.collection(u'users').document(user.id)
    doc.set(user.todict())

def delete_user(id):
    doc = db.collection(u'users').document(id).delete()
    print("deleted successfully")

#################################################################################

def create_doctor(_nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None, _department=None, _patients=None, _specialty=None):
    user = create_user(_nom,_prenom,_mobile,_address,_status,_admitDate,_profilepic)
    doc_ref = db.collection(u'doctors').document()
    doctor= Doctor(user,doc_ref.id ,_department,_patients,_specialty)
    doc_ref.set(doctor.todict())
    print("\nDoctor created succesfully ! doctor id : " + doctor.id)
    return doctor

def get_doctor(id):
    doc=db.collection('doctors').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    doctor=Doctor()
    doctor.fromdict(doc.to_dict())
    return doctor


def edit_doctor(doctor):
    doc=db.collection('doctors').document(doctor.id)
    doc.set(doctor.todict())


def delete_doctor(id):
    doc = db.collection(u'doctors').document(id).delete()
    print("deleted successfully")

#################################################################################

def create_patient(_nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None,  _staff=[], _symptoms=[],_assignedDoctorId=None):
    user = create_user(_nom,_prenom,_mobile,_address,_status,_admitDate,_profilepic)
    doc_ref = db.collection(u'patients').document()
    patient= Patient(user,doc_ref.id ,_staff,_symptoms,_assignedDoctorId)
    doc_ref.set(patient.todict())
    print("\nPatient created successfully ! patient id : " + patient.id)
    return patient
def edit_patient(patient):
    doc = db.collection('patients').document(patient.id)
    doc.set(patient.todict())

def get_patient(id):
    doc=db.collection('patients').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    patient=Patient()
    patient.fromdict(doc.to_dict())
    return patient


def delete_patient(id):
    doc = db.collection(u'patients').document(id).delete()
    print("deleted successfully")


##############################################################################


def create_staff(_nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None,  _department=None, _patients=[]):
    user = create_user(_nom,_prenom,_mobile,_address,_status,_admitDate,_profilepic)
    doc_ref = db.collection(u'staff').document()
    staff= Staff(user,doc_ref.id , _department,_patients)
    doc_ref.set(staff.todict())
    print("\nstaff created succesfully ! staff id : " + staff.id)
    return staff


def edit_staff(staff):
    doc = db.collection('staff').document(staff.id)
    doc.set(staff.todict())

def get_staff(id):
    doc=db.collection('staff').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    staff=Staff()
    staff.fromdict(doc.to_dict())
    return staff

def delete_staff(id):
    doc = db.collection(u'staff').document(id).delete()
    print("deleted successfully")