from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from .Services import *


# Create your views here.

def tolist(s):
    l = s.split(',')
    l[0] = l[0][1:]
    l[-1] = l[-1][:-1]
    return l


@csrf_exempt
@api_view(["GET"])
def doctors(request):
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        data = [i.todict() for i in get_doctors()]
        return JsonResponse(data, safe=False)
    l = tolist(ids)
    data = [i.todict() for i in get_doctorsByIDs(l)]
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(["GET"])
def patients(request):
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        data = [i.todict() for i in get_patients()]
        return JsonResponse(data, safe=False)
    l = tolist(ids)
    data = [i.todict() for i in get_patientsByIDs(l)]
    return JsonResponse(data, safe=False)


@csrf_exempt
@api_view(["GET"])
def staffs(request):
    ids = request.GET.get('ids')
    if ids == None or ids == "":
        data = [i.todict() for i in get_staffs()]
        return JsonResponse(data, safe=False)
    l = tolist(ids)
    data = [i.todict() for i in get_staffsByIDs(l)]
    return JsonResponse(data, safe=False)


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
def doctor(request):
    id = request.GET.get('id')
    if id != None:
        data = get_doctor(id).todict()
        if (data != None):
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"erreur": " no data found "})
    else:
        return JsonResponse({"erreur": " no id in url"})


@csrf_exempt
@api_view(["GET"])
def patient(request):
    id = request.GET.get('id')
    # print(id , " type  : ", type(id))
    if id != None:
        data = get_patient(id).todict()
        if (data != None):
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"erreur": " no data found "})
    else:
        return JsonResponse({"erreur": " no id in url"})


@csrf_exempt
@api_view(["GET"])
def staff(request):
    id = request.GET.get('id')
    # print(id , " type  : ", type(id))
    if id != None:
        data = get_staff(id).todict()
        if (data != None):
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"erreur": " no data found "})
    else:
        return JsonResponse({"erreur": " no id in url"})


@csrf_exempt
@api_view(["GET"])
def user(request):
    id = request.GET.get('id')
    # print(id , " type  : ", type(id))
    if id != None:
        data = get_user(id).todict()
        if (data != None):
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({"erreur": " no data found "})
    else:
        return JsonResponse({"erreur": " no id in url"})


@csrf_exempt
@api_view(["Post"])
def add_user(request):
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    user = create_user(_nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                       _status=status, _admitDate=admitDate)
    return JsonResponse(user.todict(), safe=False)


@csrf_exempt
@api_view(["Post"])
def add_patient(request):
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    staff = tolist(request.GET.get('staff'))
    symptoms = tolist(request.GET.get('symptoms'))
    print(symptoms, type(symptoms))
    assignedDoctorId = request.GET.get('assignedDoctorId')
    patient = create_patient(_nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                             _status=status, _admitDate=admitDate, _staff=staff, _symptoms=symptoms,
                             _assignedDoctorId=assignedDoctorId)
    return JsonResponse(patient, safe=False)


@csrf_exempt
@api_view(["Post"])
def add_doctor(request):
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    patients = tolist(request.GET.get('patients'))
    department = request.GET.get('department')
    specialty = request.GET.get('specialty')
    doctor = create_doctor(_nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                           _status=status, _admitDate=admitDate, _department=department, _patients=patients,
                           _specialty=specialty)
    return JsonResponse(doctor.todict(), safe=False)


@csrf_exempt
@api_view(["Post"])
def add_staff(request):
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    patients = tolist(request.GET.get('patients'))
    department = request.GET.get('department')
    staff = create_staff(_nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                         _status=status, _admitDate=admitDate, _department=department, _patients=patients)
    return JsonResponse(staff.todict(), safe=False)


@csrf_exempt
@api_view(["Post"])
def ed_staff(request):
    id = request.GET.get('id')
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    patients = tolist(request.GET.get('patients'))
    department = request.GET.get('department')

    staff = edit_staff(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                       _status=status, _admitDate=admitDate, _department=department, _patients=patients)
    return JsonResponse(staff, safe=False)


@csrf_exempt
@api_view(["Post"])
def ed_doctor(request):
    id = request.GET.get('id')
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    patients = tolist(request.GET.get('patients'))
    department = request.GET.get('department')
    specialty = request.GET.get('specialty')
    doctor = edit_doctor(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                         _status=status, _admitDate=admitDate, _department=department, _patients=patients,
                         _specialty=specialty)
    return JsonResponse(doctor.todict(), safe=False)


@csrf_exempt
@api_view(["Post"])
def ed_patient(request):
    id = request.GET.get('id')
    nom = request.GET.get('nom')
    prenom = request.GET.get('prenom')
    mobile = request.GET.get('mobile')
    address = request.GET.get('address')
    profile_pic = request.GET.get('profile_pic')
    status = request.GET.get('status')
    admitDate = request.GET.get('admitDate')
    staff = tolist(request.GET.get('staff'))
    symptoms = tolist(request.GET.get('symptoms'))
    print(symptoms, type(symptoms))
    assignedDoctorId = request.GET.get('assignedDoctorId')
    patient = edit_patient(_id=id, _nom=nom, _prenom=prenom, _mobile=mobile, _address=address, _profilepic=profile_pic,
                           _status=status, _admitDate=admitDate, _staff=staff, _symptoms=symptoms,
                           _assignedDoctorId=assignedDoctorId)
    return JsonResponse(patient, safe=False)


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
@api_view(["Post"])
def del_patient(request):
    id = request.GET.get('id')
    delete_patient(id)
    return JsonResponse({}, safe=False)


@csrf_exempt
@api_view(["Post"])
def del_doctor(request):
    id = request.GET.get('id')
    delete_doctor(id)
    return JsonResponse({}, safe=False)


@csrf_exempt
@api_view(["Post"])
def del_staff(request):
    id = request.GET.get('id')
    delete_staff(id)
    return JsonResponse({}, safe=False)


@csrf_exempt
@api_view(["Post"])
def searchUser(request):
    keyword = request.GET.get('keyword')
    users = [ i.todict() for i in get_userByName(keyword)]
    return JsonResponse(users, safe=False)


@csrf_exempt
@api_view(["Post"])
def searchPatient(request):
    keyword = request.GET.get('keyword')
    patients = [ i.todict() for i in  get_patientByName(keyword)]
    return JsonResponse(patients, safe=False)

@csrf_exempt
@api_view(["Post"])
def searchStaff(request):
    keyword = request.GET.get('keyword')
    staffs=[ i.todict() for i in get_staffByName(keyword)]
    return JsonResponse(staffs, safe=False)

@csrf_exempt
@api_view(["Post"])
def searchDoctor(request):
    keyword = request.GET.get('keyword')
    doctors=[ i.todict() for i in  get_doctorByName(keyword)]
    return JsonResponse(doctors, safe=False)


@csrf_exempt
@api_view(["Post"])
def search(request):
    keyword = request.GET.get('keyword')
    all={}
    all["staffs"]=[i.todict() for i in get_staffByName(keyword)]
    all["doctors"]=[i.todict() for i in get_doctorByName(keyword)]
    all["patients"]=[i.todict() for i in get_patientByName(keyword)]
    return JsonResponse(all, safe=False)
