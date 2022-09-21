from . import firebaseConfig
from . import models
from .firebaseConfig import *
from .models import *
import secrets
import string
alphabet = string.ascii_letters + string.digits
def generate_password():
    p=''.join(secrets.choice(alphabet) for i in range(6))
    return p

def create_user(_nom=None ,_role=None , _email=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                _profilepic=None):
    doc_ref = db.collection(u'users').document()
    password= generate_password()
    user = User(_id=doc_ref.id,_password=password ,_role=_role , _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
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

def get_userByEmail(email):
    doc = db.collection(u'users').where(u'email', u'==', email).get()[0]
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

    user = User(_id=_id, _nom=_nom, _prenom=_prenom,_password=get_user(_id).password ,_role=get_user(_id).role ,  _email=_email, _mobile=_mobile, _address=_address, _status=_status,
                _admitDate=_admitDate, _profilepic=_profilepic)
    doc = db.collection(u'users').document(user.id)
    doc.set(user.todict())
    return user


def delete_user(id):
    u = auth.get_user_by_email(get_user(id).email)
    doc = db.collection(u'users').document(id).delete()
    print("deleted successfully")


#################################################################################

def create_doctor(_nom=None, _email=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                  _profilepic=None, _department=None,  _specialty=None,
                  _rooms=None):
    user = create_user(_nom=_nom,_role="doctor" ,  _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                       _admitDate=_admitDate, _profilepic=_profilepic, _email=_email)
    doc_ref = db.collection(u'doctors').document()
    print("rooms " ,_rooms)
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
    print(" this is the get doc id "  , id)
    if not doc.exists:
        print(u'No such document!')
        print(" this is the get doc id 2 "  , id)
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
    for i in doctor.rooms:
        room=get_room(i)
        room.doctor=""
        edit_room(_id=room.id, _patients=room.patients, _department=room.department, _staff=room.staff,
                  _nbBeds=room.nbBeds, _doctor=room.doctor, _number=room.number)
    userid = doctor.user.id
    delete_user(userid)
    print(id)
    doc = db.collection(u'doctors').document(id).delete()
    print("deleted successfully")


#################################################################################

def create_patient(_nom=None, _email=None, _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                   _profilepic=None, _room=None, _symptoms=[], _weight=None , _height=None ,  _state=None , _age=None   ):
    user = create_user(_nom=_nom, _role="patient" , _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                       _admitDate=_admitDate, _profilepic=_profilepic, _email=_email)
    doc_ref = db.collection(u'patients').document()
    patient = Patient(_id=doc_ref.id,_user=user , _symptoms=_symptoms , _room=_room , _height=_height ,_age=_age , _weight=_weight , _state=_state)
    doc_ref.set(patient.todict())
    room=get_room(_room)
    room.patients.append(patient.id)
    room1=edit_room(_id=room.id , _patients=room.patients , _department=room.department ,_staff=room.staff , _nbBeds=room.nbBeds , _doctor=room.doctor , _number=room.number)
    print("\nPatient created successfully ! patient id : " + patient.id)
    return patient

def create_alert(_doctor=None ,_priority=None ,  _user=None , _createdTime=None , _responseTime=None , _content=None , _response=None   ):
    doc_ref= db.collection('alerts').document()
    alert = Alert(_id=doc_ref.id ,_priority=_priority ,  _doctor=_doctor , _user=_user , _createdTime=_createdTime , _responseTime=_responseTime , _content=_content , _response=_response )
    doc_ref.set(alert.todict())
    return alert

def edit_alert(_id=None ,_priority=None ,  _doctor=None , _user=None , _createdTime=None , _responseTime=None , _content=None , _response=None   ):
    doc_ref= db.collection('alerts').document(_id)
    alert = Alert(_id=doc_ref.id , _priority=_priority , _doctor=_doctor , _user=_user , _createdTime=_createdTime , _responseTime=_responseTime , _content=_content , _response=_response )
    doc_ref.set(alert.todict())
    return alert


def edit_patient(_id=None, _nom=None, _email=None , _prenom=None, _mobile=None, _address=None, _status=None, _admitDate=None,
                 _profilepic=None, _room=None, _symptoms=[], _weight=None , _height=None ,  _state=None , _age=None ):
    patient1 = get_patient(_id)
    userid = patient1.user.id
    user = edit_user(_id=userid,_email=_email, _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
                     _admitDate=_admitDate, _profilepic=_profilepic)
    patient = Patient(_user=user, _id=_id,  _symptoms=_symptoms , _room=_room , _height=_height , _age=_age,_weight=_weight , _state=_state)
    doc = db.collection('patients').document(patient.id)
    doc.set(patient.todict())
    if(patient1.room.strip()!=patient.room.strip()):
        oldroom=get_room(patient1.room)
        if oldroom!=None :
            print("old room   : ", oldroom.number)
            print(oldroom.patients)
            oldroom.patients.remove(patient.id)
            print(oldroom.patients)
            oldroom=edit_room(_id=oldroom.id , _patients=oldroom.patients , _department=oldroom.department ,_staff=oldroom.staff , _nbBeds=oldroom.nbBeds , _doctor=oldroom.doctor , _number=oldroom.number)
        newroom = get_room(patient.room)
        if newroom !=None :
            print("new room   : ", newroom.number)

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

def delete_alert(id):
    alert = get_alert(id)
    db.collection(u'alerts').document(id).delete()
    print("deleted successfully")


##############################################################################




def create_staff(_nom=None,_password=None ,_role=None ,  _prenom=None, _email=None , _mobile=None, _address=None, _status=None, _admitDate=None, _profilepic=None,
                 _department=None, _rooms=[]):
    user = create_user(_role="staff" , _nom=_nom, _prenom=_prenom, _mobile=_mobile, _address=_address, _status=_status,
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


def edit_staff(_id=None,  _nom=None, _prenom=None, _email=None,_mobile=None, _address=None, _status=None, _admitDate=None,
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
            print("    staffid :", staff.id, "    roomid :", room.id)
            if staff.id in  room.staff :
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
    if _doctor != None and _doctor != "":
        doctor=get_doctor(_doctor)
        doctor.rooms.append(room.id)
        doctor=edit_doctor(_id=doctor.id , _status=doctor.user.status , _admitDate=doctor.user.admitDate, _nom=doctor.user.nom, _prenom=doctor.user.prenom ,_rooms=doctor.rooms , _email=doctor.user.email , _department=doctor.department , _specialty=doctor.specialty , _address=doctor.user.address , _profilepic=doctor.user.profile_pic , _mobile=doctor.user.mobile)
    if _staff!=[] or _staff!=None :
        staffs=get_staffsByIDs(_staff)
        for staff in staffs:
            staff.rooms.append(room.id)
            staff=edit_staff(_id=staff.id ,_status=staff.user.status , _admitDate=staff.user.admitDate, _nom=staff.user.nom, _prenom=staff.user.prenom ,_rooms=staff.rooms , _email=staff.user.email , _department=staff.department ,  _address=staff.user.address , _profilepic=staff.user.profile_pic , _mobile=staff.user.mobile)
    print("\nroom created succesfully ! room id : " + room.id)
    return room



def edit_room(_id=None ,_doctor=None  , _patients=[] , _staff=[] , _department=None , _nbBeds=None , _number=None ):
    room=get_room(_id)
    room =Room(_id=_id , _doctor=_doctor , _staff=_staff , _patients=_patients,_nb_beds=_nbBeds ,_number=_number,_department=_department)
    if (_doctor!=None and _doctor!="") and (room.doctor=="" and room.doctor==None) :
        doctor=get_doctor(_doctor)
        doctor.rooms.append(_id)
        doctor=edit_doctor(_id=doctor.id, _nom=doctor.user.nom, _prenom=doctor.user.prenom, _email=doctor.user.email, _mobile=doctor.user.mobile, _address=doctor.user.address, _status=doctor.user.status,
                _admitDate=doctor.user.admitDate, _profilepic=doctor.user.profile_pic, _department=doctor.department, _rooms=doctor.rooms, _specialty=doctor.specialty)

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

def get_alerts():
    docs = db.collection(u'alerts').stream()
    alerts = []
    for doc in docs:
        alert = Alert()
        alert.fromdict(doc.to_dict())
        alerts.append(alert)
    return alerts

def get_alert(id):
    doc = db.collection('alerts').document(id).get()
    if not doc.exists:
        print(u'No such document!')
        return
    alert = Alert()
    alert.fromdict(doc.to_dict())
    return alert

def delete_staff(_id):
    staff = get_staff(_id)
    for id in staff.rooms:
        room=get_room(id)
        if room != None and staff.id in room.staff :
            room.staff.remove(staff.id)
            room=edit_room(_id=room.id , _patients=room.patients , _department=room.department ,_staff=room.staff , _nbBeds=room.nbBeds , _doctor=room.doctor , _number=room.number)
    userid = staff.user.id
    delete_user(userid)
    doc = db.collection(u'staff').document(_id).delete()
    print("deleted successfully")

def delete_room(id):
    room = get_room(id)
    doctors=get_doctors()
    patients=get_patients()
    staffs=get_staffs()
    for doctor in doctors:
        doctor.rooms=list(filter(lambda a: a !=id , doctor.rooms))
        doctor=edit_doctor(_id=doctor.id, _nom=doctor.user.nom, _prenom=doctor.user.prenom, _email=doctor.user.email, _mobile=doctor.user.mobile, _address=doctor.user.address, _status=doctor.user.status,
                _admitDate=doctor.user.admitDate, _profilepic=doctor.user.profile_pic, _department=doctor.department, _rooms=doctor.rooms, _specialty=doctor.specialty)
        for staff in staffs:
            staff.rooms = list(filter(lambda a: a != id, staff.rooms))
            staff = edit_staff(_id=staff.id, _nom=staff.user.nom, _prenom=staff.user.prenom,
                                 _email=staff.user.email, _mobile=staff.user.mobile, _address=staff.user.address,
                                 _status=staff.user.status,
                                 _admitDate=staff.user.admitDate, _profilepic=staff.user.profile_pic,
                                 _department=staff.department, _rooms=staff.rooms)
        for patient in patients:
            if patient.room==id:
                patient.room==None
                patient = edit_patient(_id=patient.id, _nom=patient.user.nom, _prenom=patient.user.prenom,
                                   _email=patient.user.email, _mobile=patient.user.mobile, _address=patient.user.address,
                                   _status=patient.user.status,
                                   _admitDate=patient.user.admitDate, _profilepic=patient.user.profile_pic,
                                   _symptoms=patient.symptoms, _room=patient.room ,_weight=patient.weight , _height=patient.height ,_state=patient.state , _age=patient.age)

    doc = db.collection(u'rooms').document(id).delete()
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

def get_alertsByIDs(ids):
    alerts = []
    for id in ids:
        alerts.append(get_staff(id))
    return alerts

## get doctors patients users and staff by ids
