from . import firebaseConfig
from . import models
from .firebaseConfig import *
from .models import *


def create_user( _nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None):
    doc_ref = db.collection(u'users').document()
    user=User(doc_ref.id ,_nom, _prenom ,_mobile, _address, _status,_admitDate, _profilepic)
    doc_ref.set(user.todict())
    print("\nUser created succesfully ! user id : " + doc_ref.id)
    return user

def get_user(id):
    doc = db.collection(u'users').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return

    user=User()
    user.fromdict(doc.to_dict())
    return user

def get_users():
    docs = db.collection(u'users').stream()
    users=[]
    for doc in docs:
        user=User()
        user.fromdict(doc.to_dict())
        users.append(user)
    return users


def edit_user(_id=None ,  _nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None):
    user=User(_id,_nom, _prenom ,_mobile, _address, _status,_admitDate, _profilepic)
    doc = db.collection(u'users').document(user.id)
    doc.set(user.todict())
    return user

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

def get_doctors():
    docs = db.collection(u'doctors').stream()
    doctors=[]
    for doc in docs:
        doctor=Doctor()
        doctor.fromdict(doc.to_dict())
        doctors.append(doctor)
    return doctors

def edit_doctor(_id=None ,_nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None, _department=None, _patients=None, _specialty=None):
    doctor1 = get_doctor(_id)
    userid = doctor1.user.id
    user =edit_user(_id=userid, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address,_status= _status, _admitDate=_admitDate, _profilepic=_profilepic)
    doctor = Doctor(_user=user,_id=_id , _department=_department , _specialty=_specialty,_patients=_patients)
    doc=db.collection('doctors').document(doctor.id)
    doc.set(doctor.todict())
    return doctor


def delete_doctor(id):
    doctor = get_doctor(id)
    print(doctor.todict())
    userid = doctor.user.id
    delete_user(userid)
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


def edit_patient(_id =None,_nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None, _assignedDoctorId=None, _staff=None , _symptoms=None):
    patient1 = get_patient(_id)
    userid = patient1.user.id
    user =edit_user(_id=userid, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address,_status= _status, _admitDate=_admitDate, _profilepic=_profilepic)
    patient= Patient(_user=user,_id=_id ,_staff=_staff , _symptoms=_symptoms , _assignedDoctorId=_assignedDoctorId)
    doc=db.collection('staff').document(patient.id)
    doc.set(patient.todict())
    return patient

def get_patient(id):
    doc=db.collection('patients').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    patient=Patient()
    patient.fromdict(doc.to_dict())
    return patient

def get_patients():
    docs = db.collection(u'patients').stream()
    patients=[]
    for doc in docs:
        patient=Patient()
        patient.fromdict(doc.to_dict())
        patients.append(patient)
    return patients

def delete_patient(id):
    patient = get_patient(id)
    userid = patient.user.id
    delete_user(userid)
    db.collection(u'patients').document(id).delete()
    print("deleted successfully")


##############################################################################


def create_staff(_nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None,  _department=None, _patients=[]):
    user = create_user(_nom,_prenom,_mobile,_address,_status,_admitDate,_profilepic)
    doc_ref = db.collection(u'staff').document()
    staff= Staff(user,doc_ref.id , _department,_patients)
    doc_ref.set(staff.todict())
    print("\nstaff created succesfully ! staff id : " + staff.id)
    return staff


def edit_staff(_id=None,_nom=None, _prenom=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None, _department=None, _patients=None):
    print("\n0")
    staff1=get_staff(_id)
    userid=staff1.user.id
    print("\n1")
    user =edit_user(_id=userid, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address,_status= _status, _admitDate=_admitDate, _profilepic=_profilepic)
    print("\n2")
    staff= Staff(_user=user,_id=_id , _department=_department ,_patients=_patients)
    print("\n3")
    doc=db.collection('staff').document(staff.id)
    print("\n4")
    doc.set(staff.todict())
    return staff

def get_staff(id):
    doc=db.collection('staff').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    staff=Staff()
    staff.fromdict(doc.to_dict())
    return staff

def get_staffs():
    docs = db.collection(u'staff').stream()
    staffs=[]
    for doc in docs:
        staff=Staff()
        staff.fromdict(doc.to_dict())
        staffs.append(staff)
    return staffs

def delete_staff(id):
    staff = get_staff(id)
    userid = staff.user.id
    delete_user(userid)
    doc = db.collection(u'staff').document(id).delete()
    print("deleted successfully")