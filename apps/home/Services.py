from . import firebaseConfig
from . import models
from .firebaseConfig import *
from .models import *


def create_user(_nom=None, _email=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                _profilepic=None):
    doc_ref = db.collection(u'users').document()
    user = User(_id=doc_ref.id, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                _admitDate=_admitDate, _profilepic=_profilepic, _email=_email)
    doc_ref.set(user.todict())
    print("\nUser created succesfully ! user id : " + doc_ref.id)
    return user


def get_user(id):
    doc = db.collection(u'users').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return

    user = User()
    user.fromdict(doc.to_dict())
    return user


def get_users():
    docs = db.collection(u'users').stream()
    users = []
    for doc in docs:
        user = User()
        user.fromdict(doc.to_dict())
        users.append(user)
    return users


def edit_user(_id=None, _email=None, _nom=None, _prenom=None, _mobile=None, _address=None, _status=None,
              _admitDate=None, _profilepic=None):
    user = User(_id=_id, _nom=_nom, _prenom=_prenom, _email=_email, _mobile=_mobile, _address=_address, _status=_status,
                _admitDate=_admitDate, _profilepic=_profilepic)
    doc = db.collection(u'users').document(user.id)
    doc.set(user.todict())
    return user


def delete_user(id):
    doc = db.collection(u'users').document(id).delete()
    print("deleted successfully")


#################################################################################

def create_doctor(_nom=None, _email=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                  _profilepic=None, _department=None,  _specialty=None,
                  _rooms=None):
    user = create_user(_nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                       _admitDate=_admitDate, _profilepic=_profilepic, _email=_email)
    doc_ref = db.collection(u'doctors').document()
    doctor = Doctor(_user=user, _id=doc_ref.id, _department=_department, _rooms=_rooms, _specialty=_specialty)
    doc_ref.set(doctor.todict())
    if doctor.rooms!=[]:
        rooms=get_roomsByIDs(doctor.rooms)
        for room in rooms:
            room.doctor=doctor.id
            room1=edit_room(_id=room.id , _patients=room.patients , _department=room.department ,_staff=room.staff , _nbBeds=room.nbBeds , _doctor=room.doctor , _number=room.number)
    print("\nDoctor created succesfully ! doctor id : " + doctor.id)
    return doctor


def get_doctor(id):
    doc = db.collection('doctors').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    doctor = Doctor()
    doctor.fromdict(doc.to_dict())
    return doctor


def get_doctors():
    docs = db.collection(u'doctors').stream()
    doctors = []
    for doc in docs:
        doctor = Doctor()
        doctor.fromdict(doc.to_dict())
        doctors.append(doctor)
    return doctors


def edit_doctor(_id=None, _nom=None, _prenom=None, _email=None, _mobile=None, _address=None, _status=None,
                _admitDate=None, _profilepic=None, _department=None, _rooms=None, _specialty=None):
    doctor1 = get_doctor(_id)
    userid = doctor1.user.id
    user = edit_user(_id=userid, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                     _admitDate=_admitDate, _profilepic=_profilepic, _email=_email)

    doctor = Doctor(_user=user, _id=_id, _department=_department, _specialty=_specialty, _rooms=_rooms)
    doc = db.collection('doctors').document(doctor.id)
    doc.set(doctor.todict())
    if list(set(doctor1.rooms) - set(doctor.rooms))!=[]:
        for newroom in list(set(doctor.rooms) - set(doctor1.rooms)) :
            room = get_room(newroom)
            room.doctor=doctor.id
            room = edit_room(_id=room.id, _patients=room.patients, _department=room.department,
                                _staff=room.staff, _nbBeds=room.nbBeds, _doctor=room.doctor,
                                _number=room.number)
        for oldroom in list(set(doctor1.rooms) - set(doctor.rooms)):
            room=get_room(oldroom)
            room.doctor=""
            room = edit_room(_id=room.id, _patients=room.patients, _department=room.department,
                                _staff=room.staff, _nbBeds=room.nbBeds, _doctor=room.doctor,
                                _number=room.number)

    return doctor


def delete_doctor(id):
    doctor = get_doctor(id)
    print(doctor.todict())
    userid = doctor.user.id
    delete_user(userid)
    doc = db.collection(u'doctors').document(id).delete()
    print("deleted successfully")


#################################################################################

def create_patient(_nom=None, _email=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                   _profilepic=None, _room=None, _symptoms=[], _weight=None , _height=None ,  _state=None , _age=None   ):
    user = create_user(_nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                       _admitDate=_admitDate, _profilepic=_profilepic, _email=_email)
    doc_ref = db.collection(u'patients').document()
    patient = Patient(_id=doc_ref.id,_user=user , _symptoms=_symptoms , _room=_room , _height=_height ,_age=_age , _weight=_weight , _state=_state)
    doc_ref.set(patient.todict())
    room=get_room(_room)
    room.patients.append(patient.id)
    room1=edit_room(_id=room.id , _patients=room.patients , _department=room.department ,_staff=room.staff , _nbBeds=room.nbBeds , _doctor=room.doctor , _number=room.number)
    print("\nPatient created successfully ! patient id : " + patient.id)
    return patient


def edit_patient(_id=None, _nom=None, _email=None , _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                 _profilepic=None, _room=None, _symptoms=[], _weight=None , _height=None ,  _state=None , _age=None ):
    patient1 = get_patient(_id)
    userid = patient1.user.id
    user = edit_user(_id=userid,_email=_email, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                     _admitDate=_admitDate, _profilepic=_profilepic)
    patient = Patient(_user=user, _id=_id,  _symptoms=_symptoms , _room=_room , _height=_height , _age=_age,_weight=_weight , _state=_state)
    doc = db.collection('patients').document(patient.id)
    doc.set(patient.todict())
    if(patient1.room!=patient.room):
        oldroom=get_room(patient1.room)
        oldroom.patients.remove(patient1.id)
        oldroom=edit_room(_id=oldroom.id , _patients=oldroom.patients , _department=oldroom.department ,_staff=oldroom.staff , _nbBeds=oldroom.nbBeds , _doctor=oldroom.doctor , _number=oldroom.number)
        newroom = get_room(patient1.room)
        newroom.patients.append(patient.id)
        newroom = edit_room(_id=newroom.id, _patients=newroom.patients, _department=newroom.department,
                            _staff=newroom.staff, _nbBeds=newroom.nbBeds, _doctor=newroom.doctor,
                            _number=newroom.number)
    return patient


def get_patient(id):
    doc = db.collection('patients').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    patient = Patient()
    patient.fromdict(doc.to_dict())
    return patient


def get_patients():
    docs = db.collection(u'patients').stream()
    patients = []
    for doc in docs:
        patient = Patient()
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


def create_staff(_nom=None, _prenom=None, _email=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None,
                 _department=None, _rooms=[]):
    user = create_user(_nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                       _admitDate=_admitDate, _profilepic=_profilepic, _email=_email)
    doc_ref = db.collection(u'staff').document()
    staff = Staff(_user=user, _id=doc_ref.id,_department= _department, _rooms=_rooms)
    doc_ref.set(staff.todict())
    if staff.rooms!=[] :
        rooms=get_roomsByIDs(staff.rooms)
        for room in rooms:
            room.staff.append(staff.id)
            room1=edit_room(_id=room.id , _patients=room.patients , _department=room.department ,_staff=room.staff , _nbBeds=room.nbBeds , _doctor=room.doctor , _number=room.number)
    print("\nstaff created succesfully ! staff id : " + staff.id)
    return staff


def edit_staff(_id=None, _nom=None, _prenom=None, _email=None,_mobile=None, _address=None, _status=None, _admitDate=None,
               _profilepic=None,  _department=None, _rooms=[]):
    staff1 = get_staff(_id)
    userid = staff1.user.id

    user = edit_user(_id=userid, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                     _admitDate=_admitDate, _profilepic=_profilepic , _email=_email)

    staff = Staff(_user=user, _id=_id, _department=_department, _rooms=_rooms)
    doc = db.collection('staff').document(staff.id)
    if list(set(staff1.rooms) - set(staff.rooms))!=[]:
        for newroom in list(set(staff.rooms) - set(staff1.rooms)) :
            room = get_room(newroom)
            room.staff.append(staff.id)
            room = edit_room(_id=room.id, _patients=room.patients, _department=room.department,
                                _staff=room.staff, _nbBeds=room.nbBeds, _doctor=room.doctor,
                                _number=room.number)
        for oldroom in list(set(staff1.rooms) - set(staff.rooms)):
            room=get_room(oldroom)
            room.staff.remove(staff.id)
            room = edit_room(_id=room.id, _patients=room.patients, _department=room.department,
                                _staff=room.staff, _nbBeds=room.nbBeds, _doctor=room.doctor,
                                _number=room.number)
    doc.set(staff.todict())
    return staff


def get_staff(id):
    doc = db.collection('staff').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    staff = Staff()
    staff.fromdict(doc.to_dict())
    return staff

def create_room(_doctor=None  , _patients=[] , _staff=[] , _department=None , _nbBeds=None , _number=None  ):
    doc_ref = db.collection(u'rooms').document()
    room=Room(_id=doc_ref.id , _doctor=_doctor , _staff=_staff , _patients=_patients,_nb_beds=_nbBeds ,_number=_number,_department=_department)
    doc_ref.set(room.todict())
    doctor=get_doctor(_doctor)
    doctor.rooms.append(room.id)
    doctor=edit_doctor(_id=doctor.id , _status=doctor.user.status , _admitDate=doctor.user.admitDate, _nom=doctor.user.nom, _prenom=doctor.user.prenom ,_rooms=doctor.rooms , _email=doctor.user.email , _department=doctor.department , _specialty=doctor.specialty , _address=doctor.user.address , _profilepic=doctor.user.profile_pic , _mobile=doctor.user.mobile)
    staffs=get_staffsByIDs(_staff)
    for staff in staffs:
        staff.rooms.append(room.id)
        staff=edit_staff(_id=staff.id ,_status=staff.user.status , _admitDate=staff.user.admitDate, _nom=staff.user.nom, _prenom=staff.user.prenom ,_rooms=staff.rooms , _email=staff.user.email , _department=staff.department ,  _address=staff.user.address , _profilepic=staff.user.profile_pic , _mobile=staff.user.mobile)
    print("\nroom created succesfully ! room id : " + room.id)
    return room



def edit_room(_id=None ,_doctor=None  , _patients=[] , _staff=[] , _department=None , _nbBeds=None , _number=None ):
    room=get_room(_id)
    room =Room(_id=_id , _doctor=_doctor , _staff=_staff , _patients=_patients,_nb_beds=_nbBeds ,_number=_number,_department=_department)
    doc = db.collection('rooms').document(room.id)
    doc.set(room.todict())
    return room



def get_room(id):
    doc = db.collection('rooms').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    room = Room()
    room.fromdict(doc.to_dict())
    return room

def get_rooms():
    docs = db.collection(u'rooms').stream()
    rooms = []
    for doc in docs:
        room = Room()
        room.fromdict(doc.to_dict())
        rooms.append(room)
    return rooms

def get_staffs():
    docs = db.collection(u'staff').stream()
    staffs = []
    for doc in docs:
        staff = Staff()
        staff.fromdict(doc.to_dict())
        staffs.append(staff)
    return staffs


def delete_staff(id):
    staff = get_staff(id)
    userid = staff.user.id
    delete_user(userid)
    doc = db.collection(u'staff').document(id).delete()
    print("deleted successfully")


def get_userByName(s=""):
    s = s.strip()
    if (s == ""):
        return
    users = get_users()
    users1 = []
    for user in users:
        if (user.nom.find(s) != -1 or user.prenom.find(s) != -1):
            users1.append(user)
    return users1


def get_patientByName(s):
    s = s.strip()
    if s == "":
        return
    patients = get_patients()
    patients1 = []
    for patient in patients:
        if (patient.user.nom.find(s) != -1 or patient.user.prenom.find(s) != -1):
            patients1.append(patient)
    return patients1


def get_doctorByName(s):
    s = s.strip()
    if s == "":
        return
    doctors = get_doctors()
    doctors1 = []
    for doctor in doctors:
        if (doctor.user.nom.find(s) != -1 or doctor.user.prenom.find(s) != -1):
            doctors1.append(doctor)
    return doctors1


def get_staffByName(s):
    s = s.strip()
    if s == "":
        return
    staffs = get_staffs()
    staffs1 = []
    for staff in staffs:
        if (staff.user.nom.find(s) != -1 or staff.user.prenom.find(s) != -1):
            staffs1.append(staff)
    return staffs1


def get_usersByIDs(ids):
    users = []
    for id in ids:
        users.append(get_user(id))
    return users

def get_roomsByIDs(ids):
    rooms= []
    for id in ids:
        rooms.append(get_room(id))
    return rooms

def get_patientsByIDs(ids):
    patients = []
    for id in ids:
        patients.append(get_patient(id))
    return patients


def get_doctorsByIDs(ids):
    doctors = []
    for id in ids:
        doctors.append(get_doctor(id))
    return doctors


def get_staffsByIDs(ids):
    staffs = []
    for id in ids:
        staffs.append(get_staff(id))
    return staffs

## get doctors patients users and staff by ids
