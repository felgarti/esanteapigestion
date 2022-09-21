# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from datetime import date
from datetime import datetime
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .Services import *

currentuser=None

@csrf_exempt
def login_view(request):
    global currentuser
    if (request.method == "GET"):
        return render(request, 'home/sign-in.html')
    if (request.method == "POST"):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = get_userByEmail(email)
        if user!=None and user.password==password :
            currentuser=get_userByEmail(email)
            print(email , currentuser.email)
            return redirect(index)
        else:
            return render(request, 'home/sign-in.html')




@csrf_exempt
def logout_view(request):
    global currentuser
    currentuser=None
    return redirect(login_view)


@csrf_exempt
@login_required(login_url="/login/")
def index(request):
    role=currentuser.role
    capacite = 50
    context = {'role':role , 'segment': 'index', "capacite": capacite, "patients": get_patients(), "nb_staff": len(get_staffs()),
               "nb_doctors": len(get_doctors()), "nb_patients": len(get_patients()),
               "rate": int((len(get_patients()) / capacite) * 100) ,"nbrooms":len(get_rooms()) , "alerts" : get_alerts() }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def tolist(s):
    l = s.split('\n')
    return l


@csrf_exempt
@api_view(["GET"])
def doctors(request):
    global currentuser
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        doctors = get_doctors()
        print(currentuser.email)
        return render(request, 'home/doctors.html', {"segment": "doctors", "doctors": doctors})
    l = tolist(ids)

    # data = [i.todict() for i in get_doctorsByIDs(l)]

    doctors = get_doctorsByIDs(l)
    return render(request, 'home/doctors.html', {"segment": "doctors", "doctors": doctors})


@csrf_exempt
@api_view(["GET"])
def patients(request):
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        data = [i for i in get_patients()]
        return render(request, 'home/patients.html', {"segment": "patients", "patients": data})
    l = tolist(ids)
    data = [i for i in get_patientsByIDs(l)]
    return render(request, 'home/patients.html', {"segment": "patients", "patients": data})


@csrf_exempt
@api_view(["GET"])
def staffs(request):
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        data = [i for i in get_staffs()]
        return render(request, 'home/staffs.html', {"segment": "staffs", "staffs": data})
    l = tolist(ids)
    data = [i for i in get_staffsByIDs(l)]
    return render(request, 'home/staffs.html', {"segment": "staffs", "staffs": data})


@csrf_exempt
@api_view(["GET"])
def users(request):
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        data = [i.todict() for i in get_users()]
        return JsonResponse(data, safe=False)
    l = tolist(ids)
    data = [i.todict() for i in get_usersByIDs(l)]
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(["GET"])
def patientProfile(request):
    id = request.GET.get('id')
    patient = get_patient(id)
    room=None
    doctor=None
    if patient.room!=None and patient.room!="":
        print("room : " , patient.room)
        room = get_room(patient.room)
        staffs=[]
        if room !=None :
            roomnumber = room.number
            staffs = get_staffsByIDs(room.staff)
            if room.doctor != None and room.doctor != "":
                doctor = get_doctor(room.doctor)
        else:
            roomnumber = ""


    return render(request, 'home/patientProfile.html',
                  {"segment": "", "patient": patient, "doctor": doctor, "staffs": staffs, "roomnumber": roomnumber})


@csrf_exempt
@api_view(["GET"])
def doctorProfile(request):
    id = request.GET.get('id')
    doctor = get_doctor(id)
    rooms = get_roomsByIDs(doctor.rooms)
    patients = []
    for room in rooms:
        patients+=get_patientsByIDs(room.patients)
    return render(request, 'home/doctorProfile.html',
                  {"segment": "", "patients": patients, "nbrooms": len(rooms), "nbpatients": len(patients),
                   "doctor": doctor, "rooms": rooms})


@csrf_exempt
@api_view(["GET"])
def staffProfile(request):
    id = request.GET.get('id')
    staff = get_staff(id)
    rooms = get_roomsByIDs(staff.rooms)
    patients = []
    for room in rooms:
        patients+=get_patientsByIDs(room.patients)

    return render(request, 'home/staffProfile.html',
                  {"segment": "", "patients": patients, "nbrooms": len(rooms), "nbpatients": len(patients),
                   "staff": staff, "rooms": rooms})


#
# @csrf_exempt
# @api_view(["GET"])
# def doctor(request):
#     id = request.GET.get('id')
#     if id != None:
#         data = get_doctor(id).todict()
#         if (data != None):
#             return JsonResponse(data, safe=False)
#         else:
#             return JsonResponse({"erreur": " no data found "})
#     else:
#         return JsonResponse({"erreur": " no id in url"})
#
#
# @csrf_exempt
# @api_view(["GET"])
# def patient(request):
#     id = request.GET.get('id')
#     # print(id , " type  : ", type(id))
#     if id != None:
#         data = get_patient(id).todict()
#         if (data != None):
#             return JsonResponse(data, safe=False)
#         else:
#             return JsonResponse({"erreur": " no data found "})
#     else:
#         return JsonResponse({"erreur": " no id in url"})


# @csrf_exempt
# @api_view(["GET"])
# def staff(request):
#     id = request.GET.get('id')
#     # print(id , " type  : ", type(id))
#     if id != None:
#         data = get_staff(id).todict()
#         if (data != None):
#             return JsonResponse(data, safe=False)
#         else:
#             return JsonResponse({"erreur": " no data found "})
#     else:
#         return JsonResponse({"erreur": " no id in url"})


# @csrf_exempt
# @api_view(["GET"])
# def user(request):
#     id = request.GET.get('id')
#     # print(id , " type  : ", type(id))
#     if id != None:
#         data = get_user(id).todict()
#         if (data != None):
#             return JsonResponse(data, safe=False)
#         else:
#             return JsonResponse({"erreur": " no data found "})
#     else:
#         return JsonResponse({"erreur": " no id in url"})


# @csrf_exempt
# @api_view(["Post"])
# def add_user(request):
#     nom = request.GET.get('nom')
#     prenom = request.GET.get('prenom')
#     mobile = request.GET.get('mobile')
#     address = request.GET.get('address')
#     profile_pic = request.GET.get('profile_pic')
#     status = request.GET.get('status')
#     admitDate = request.GET.get('admitDate')
#     user = create_user(_nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
#                        _status=status, _admitDate=admitDate)
#     return JsonResponse(user.todict(), safe=False)


@csrf_exempt
def addAlert(request):
    if (request.method == "GET"):

        return render(request, 'home/addAlert.html')
    if (request.method == "POST"):
        content = request.POST.get('content')
        priority=request.POST.get('priority')
        user=currentuser.id # to replace
        createdTime=str(datetime.now().strftime("%H:%M:%S"))
        alert = create_alert(_doctor=None , _createdTime=createdTime , _responseTime=None , _response=None , _user=user , _content=content ,_priority=priority)
        return redirect(index)

@csrf_exempt
def respondAlert(request):
    if (request.method == "GET"):
        _id = request.GET.get('id')
        print(_id , "this is id of the alert ")
        return render(request, 'home/respondAlert.html', {"alert" : get_alert(_id)})
    if (request.method == "POST"):
        _id = request.POST.get('id')
        print(_id, "this is id of the alert 2")
        alert= get_alert(_id)
        response = request.POST.get('response')
        responseTime=str(datetime.now().strftime("%H:%M:%S"))
        content = alert.content
        priority= alert.priority
        user=alert.user
        # to replace
        doctor=currentuser.id
        createdTime=alert.createdTime
        alert = edit_alert(_id=_id, _doctor=doctor , _createdTime=createdTime , _responseTime=responseTime , _response=response , _user=user , _content=content ,_priority=priority)
        return redirect(index)




@csrf_exempt
def addPatient(request):
    if (request.method == "GET"):
        rooms = get_rooms()
        available = []
        for room in rooms:
            if (room.nbBeds !="") and (int(room.nbBeds) - len(room.patients) != 0):
                available.append(room)
        return render(request, 'home/addPatient.html', {"rooms": available})
    if (request.method == "POST"):
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        prenom = request.POST.get('prenom')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic', '')
        status = request.POST.get('status')
        admitDate = str(date.today())
        weight = request.POST.get('weight',0)
        height = request.POST.get('height',0)
        age = request.POST.get('age',0)
        print(age)
        state = request.POST.get('state',0)
        room = request.POST.get('room',None)
        symptoms = tolist(request.POST.get('symptoms'))

        print(symptoms, type(symptoms))

        patient = create_patient(_nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                                 _status=status, _admitDate=admitDate, _symptoms=symptoms, _weight=weight, _email=email,
                                 _height=height, _state=state, _room=room, _age=age)
        return redirect(patients)


@csrf_exempt
def editPatient(request):
    if (request.method == "GET"):
        id = request.GET.get('id')
        patient = get_patient(id)
        rooms = get_rooms()
        available = []
        for room in rooms:
            if int(room.nbBeds) - len(room.patients) != 0:
                available.append(room)
        if patient.room not in [i.id for i in available]:
            available.append(get_room(patient.room))
        roomnumber=get_room(patient.room)
        if roomnumber!=None :
            roomnumber=roomnumber.number
        else:
            roomnumber=""
        return render(request, 'home/editPatient.html',
                      {"patient": patient, "rooms": available, "currentroom": roomnumber})
    if (request.method == "POST"):
        id = request.POST.get('id')
        patient = get_patient(id)
        print(patient.user.address)
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        age = request.POST.get('age')
        state = request.POST.get('state')
        room = request.POST.get('room')
        prenom = request.POST.get('prenom')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic', '')
        status = request.POST.get('status')
        admitDate = patient.user.admitDate
        symptoms = tolist(request.POST.get('symptoms'))
        patient = edit_patient(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address,
                               _profilepic=profile_pic,
                               _status=status, _admitDate=admitDate, _height=height, _weight=weight, _state=state,
                               _email=email, _symptoms=symptoms, _room=room, _age=age)

        return redirect(patients)


@csrf_exempt
def addDoctor(request):
    if (request.method == "GET"):
        rooms = get_rooms()
        available = []
        for room in rooms:
            if room.doctor == "" or room.doctor == None:
                available.append(room)
        return render(request, 'home/addDoctor.html', {"rooms": available})
    if (request.method == "POST"):
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic', '')
        status = request.POST.get('status')
        admitDate = str(date.today())
        rooms = []  # will change
        for id in [i.id for i in get_rooms()]:
            if (request.POST.get(id) != None):
                rooms.append(request.POST.get(id))
        department = request.POST.get('department')
        specialty = request.POST.get('specialty')
        doctor = create_doctor(_nom=nom, _prenom=prenom, _email=email , _mobile=mobile, _address=address, _profilepic=profile_pic,
                               _status=status, _admitDate=admitDate, _department=department, _rooms=rooms,
                               _specialty=specialty)
        return redirect(doctors)


@csrf_exempt
def addStaff(request):
    if (request.method == "GET"):
        rooms = get_rooms()
        available = []
        for room in rooms:
            available.append({"number":room.number , "nbstaff" : len(room.staff) ,"id":room.id})
        return render(request, 'home/addStaff.html',{"rooms": available})
    if (request.method == "POST"):
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic', '')
        status = request.POST.get('status')
        admitDate = str(date.today())
        rooms = [] # will change
        for id in [i.id for i in get_rooms()]:
            if(request.POST.get(id)!=None):
                rooms.append(request.POST.get(id))
        print(rooms[0])
        department = request.POST.get('department')
        doctor = create_staff(_nom=nom, _prenom=prenom, _email=email, _mobile=mobile, _address=address,
                               _profilepic=profile_pic,
                               _status=status, _admitDate=admitDate, _department=department, _rooms=rooms)
        return redirect(staffs)

@csrf_exempt
def editStaff(request):
    if (request.method == "GET"):
        id = request.GET.get('id')
        staff = get_staff(id)
        checked = get_roomsByIDs(staff.rooms)

        rooms=[]
        for i in [i.id for i in get_rooms()]:
            if i not in staff.rooms:
                rooms.append(get_room(i))

        return render(request, 'home/editStaff.html', {"staff": staff , "rooms":rooms , "checked_rooms":checked})
    if (request.method == "POST"):
        id = request.POST.get('id')
        staff = get_staff(id)
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic', '')
        status = request.POST.get('status')
        admitDate = staff.user.admitDate
        rooms = []  # checkbox will change
        for id in [i.id for i in get_rooms()]:
            if (request.POST.get(id) != None):
                rooms.append(request.POST.get(id))
        department = request.POST.get('department')
        staff = edit_staff(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                           _status=status, _admitDate=admitDate, _department=department , _rooms=rooms , _email=email)
        return redirect(staffs)


@csrf_exempt
def editDoctor(request):
    if (request.method == "GET"):
        id = request.GET.get('id')
        doctor = get_doctor(id)
        checked = get_roomsByIDs(doctor.rooms)
        rooms = []
        for i in [i.id for i in get_rooms()]:
            if i not in doctor.rooms:
                rooms.append(get_room(i))
        return render(request, 'home/editDoctor.html', {"doctor": doctor,"rooms":rooms , "checked_rooms":checked})
    if (request.method == "POST"):
        _id = request.POST.get('id')
        print("yyyyyyyyyyyyyyo" , _id)
        doctor = get_doctor(_id)
        email = request.POST.get('email')
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        profile_pic = request.POST.get('profile_pic', '')
        status = request.POST.get('status')
        admitDate = doctor.user.admitDate
        rooms = []  # checkbox will change
        for id in [i.id for i in get_rooms()]:
            if (request.POST.get(id) != None):
                rooms.append(request.POST.get(id))
        department = request.POST.get('department')
        specialty = request.POST.get('specialty')
        doctor = edit_doctor(_id=_id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address,
                             _profilepic=profile_pic,
                             _status=status, _admitDate=admitDate, _department=department, _rooms=rooms, _email=email,
                             _specialty=specialty)
        return redirect(doctors)




@csrf_exempt
@api_view(["GET"])
def rooms(request):
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        data = get_rooms()
        return render(request, 'home/rooms.html', {"segment": "rooms", "rooms": data})
    l = tolist(ids)
    data = get_staffsByIDs(l)
    return render(request, 'home/rooms.html', {"segment": "rooms", "rooms": data})

@csrf_exempt
def addRoom(request):
    if (request.method == "GET"):
        doctors = get_doctors()
        staffs=get_staffs()
        rooms1=[]
        for staff in staffs:
            rooms1.append(len(staff.rooms))
        list_staff = zip(staffs, rooms1)
        return render(request, 'home/addRoom.html',{"doctors": doctors , "list_staff":list_staff})
    if (request.method == "POST"):
        nbbeds = request.POST.get('nbBeds')
        number = request.POST.get('number')
        doctor = request.POST.get('doctor')
        department = request.POST.get('department')
        staff=[] # checkbox will change
        for id in [i.id for i in get_staffs()] :
            if (request.POST.get(id) != None):
                staff.append(request.POST.get(id))
        print(request.POST.get("0C7MxmPVcyEgbSWYXPOP"))
        room = create_room( _number=number, _doctor=doctor, _department=department, _staff=staff ,_patients=[] , _nbBeds=nbbeds)
        return redirect(rooms)



@csrf_exempt
def editRoom(request):
    if (request.method == "GET"):
        id = request.GET.get('id')
        room=get_room(id)
        checked=get_staffsByIDs(room.staff)
        doctors = get_doctors()
        staffs=[]
        for i in [i.id for i in  get_staffs()]:
            if i not in room.staff:
                staffs.append(get_staff(i))
        rooms1=[]
        rooms2=[]
        for staff in staffs:
            rooms1.append(len(staff.rooms))
        for st in checked:
            rooms2.append(len(st.rooms))
        list_staff = zip(staffs, rooms1)
        list_checked = zip(checked, rooms2)
        doctor=None
        if room.doctor!=None and room.doctor!="" :
            doctor=get_doctor(room.doctor)
        return render(request, 'home/editRoom.html',{"room": room ,"currentdoctor":doctor ,  "doctors": doctors ,"list_checked":list_checked ,  "list_staff":list_staff})
    if (request.method == "POST"):
        id = request.POST.get('id')
        room=get_room(id)
        print("id   " ,id)
        nbbeds = request.POST.get('nbBeds')
        number = request.POST.get('number')
        doctor = request.POST.get('doctor')
        department = request.POST.get('department')
        staff=[] # checkbox will change
        for id in [i.id for i in get_staffs()] :
            if (request.POST.get(id) != None):
                staff.append(request.POST.get(id))

        room = edit_room(_id=id ,  _number=number, _doctor=doctor, _department=department, _staff=staff ,_patients=room.patients , _nbBeds=nbbeds)
        return redirect(rooms)


# @csrf_exempt
# @api_view(["Post"])
# def ed_staff(request):
#     id = request.GET.get('id')
#     nom = request.GET.get('nom')
#     prenom = request.GET.get('prenom')
#     mobile = request.GET.get('mobile')
#     address = request.GET.get('address')
#     profile_pic = request.GET.get('profile_pic')
#     status = request.GET.get('status')
#     admitDate = request.GET.get('admitDate')
#     patients = tolist(request.GET.get('patients'))
#     department = request.GET.get('department')
#
#     staff = edit_staff(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
#                        _status=status, _admitDate=admitDate, _department=department, _patients=patients)
#     return JsonResponse(staff, safe=False)


# @csrf_exempt
# @api_view(["Post"])
# def ed_doctor(request):
#     id = request.GET.get('id')
#     nom = request.GET.get('nom')
#     prenom = request.GET.get('prenom')
#     mobile = request.GET.get('mobile')
#     address = request.GET.get('address')
#     profile_pic = request.GET.get('profile_pic')
#     status = request.GET.get('status')
#     admitDate = request.GET.get('admitDate')
#     patients = tolist(request.GET.get('patients'))
#     department = request.GET.get('department')
#     specialty = request.GET.get('specialty')
#     doctor = edit_doctor(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
#                          _status=status, _admitDate=admitDate, _department=department, _patients=patients,
#                          _specialty=specialty)
#     return JsonResponse(doctor.todict(), safe=False)


# @csrf_exempt
# @api_view(["Post"])
# def ed_patient(request):
#     id = request.GET.get('id')
#     nom = request.GET.get('nom')
#     prenom = request.GET.get('prenom')
#     mobile = request.GET.get('mobile')
#     address = request.GET.get('address')
#     profile_pic = request.GET.get('profile_pic')
#     status = request.GET.get('status')
#     admitDate = request.GET.get('admitDate')
#     staff = tolist(request.GET.get('staff'))
#     symptoms = tolist(request.GET.get('symptoms'))
#     print(symptoms, type(symptoms))
#     assignedDoctorId = request.GET.get('assignedDoctorId')
#     patient = edit_patient(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
#                            _status=status, _admitDate=admitDate, _staff=staff, _symptoms=symptoms,
#                            _assignedDoctorId=assignedDoctorId)
#     return JsonResponse(patient, safe=False)


@csrf_exempt
@api_view(["Post"])
def ed_user(request):
    id = request.GET.get('id')
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    user = edit_user(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                     _status=status, _admitDate=admitDate)
    return JsonResponse(user.todict(), safe=False)


@csrf_exempt
@api_view(["Post"])
def del_user(request):
    id = request.GET.get('id')
    delete_user(id)
    return JsonResponse({}, safe=False)


@csrf_exempt
def del_alert(request):
    id = request.GET.get('id')
    delete_alert(id)
    return redirect(index)

@csrf_exempt
def del_patient(request):
    id = request.GET.get('id')
    delete_patient(id)
    return redirect(patients)

@csrf_exempt
def del_room(request):
    id = request.GET.get('id')
    delete_room(id)
    return redirect(rooms)


# , {"segment":"patients" ,"patients":get_patients()}


@csrf_exempt
def del_doctor(request):
    id = request.GET.get('id')
    print("yyoooooooooooooooo" ,id)
    delete_doctor(id)
    return redirect(doctors)


@csrf_exempt
def del_staff(request):
    id = request.GET.get('id')
    delete_staff(id)
    return redirect(staffs)


@csrf_exempt
@api_view(["Post"])
def searchUser(request):
    keyword = request.GET.get('keyword')
    users = [i.todict() for i in get_userByName(keyword)]
    return JsonResponse(users, safe=False)


@csrf_exempt
@api_view(["Post"])
def searchPatient(request):
    keyword = request.GET.get('keyword')
    patients = [i.todict() for i in get_patientByName(keyword)]
    return JsonResponse(patients, safe=False)


@csrf_exempt
@api_view(["Post"])
def searchStaff(request):
    keyword = request.GET.get('keyword')
    staffs = [i.todict() for i in get_staffByName(keyword)]
    return JsonResponse(staffs, safe=False)


@csrf_exempt
@api_view(["Post"])
def searchDoctor(request):
    keyword = request.GET.get('keyword')
    doctors = [i.todict() for i in get_doctorByName(keyword)]
    return JsonResponse(doctors, safe=False)


@csrf_exempt
@api_view(["Post"])
def search(request):
    keyword = request.GET.get('keyword')
    all = {}
    all["staffs"] = [i.todict() for i in get_staffByName(keyword)]
    all["doctors"] = [i.todict() for i in get_doctorByName(keyword)]
    all["patients"] = [i.todict() for i in get_patientByName(keyword)]
    return JsonResponse(all, safe=False)
