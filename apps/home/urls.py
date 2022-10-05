# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from apps.home import views

urlpatterns = [

    # The home page
    path('index.html', views.index, name='home'),
    path('', views.index, name='home'),
    # Matches any html file
    # re_path(r'^.*\.*', views.pages, name='pages'),
    path('doctors.html', views.doctors),
    path('patients.html', views.patients),
    path('staffs.html', views.staffs),
    path('rooms.html', views.rooms),
    path('profile/', views.profile , name='profile'),
    path('patientProfile.html', views.patientProfile),
    path('doctorProfile.html', views.doctorProfile),
    path('staffProfile.html', views.staffProfile),
    path('addPatient.html', views.addPatient, name='addPatient'),
    path('addRoom.html', views.addRoom, name='addRoom'),
    path('addAlert.html', views.addAlert, name='addAlert'),
    path('respondAlert.html', views.respondAlert, name='respondAlert'),
    path('editRoom.html', views.editRoom, name='editRoom'),
    path('addDoctor.html', views.addDoctor, name='addDoctor'),
    path('addStaff.html', views.addStaff, name='addStaff'),
    path('editPatient.html', views.editPatient, name="editPatient"),
    path('editDoctor.html', views.editDoctor, name="editDoctor"),
    path('editStaff.html', views.editStaff, name="editStaff"),
    # path('users/', views.users),
    # path('doctor/', views.doctor),
    # path('patient/', views.patient),
    # path('staff/', views.staff),
    # path('user/', views.user),
    # path('add_user/', views.add_user),
    # path('add_patient/', views.add_patient),
    # path('add_staff/', views.add_staff),
    # path('add_doctor/', views.add_doctor),

    path('searchUser/', views.searchUser),
    path('searchPatient/', views.searchPatient),
    path('searchStaff/', views.searchStaff),
    path('searchDoctor/', views.searchDoctor),
    path('search/', views.search),

    # path('edit_user/', views.ed_user),
    # # path('edit_patient/', views.ed_patient),
    # path('edit_staff/', views.ed_staff),
    # path('edit_doctor/', views.ed_doctor),

    # path('delete_user?id=<slug:id>', views.del_user),
    path('delete_patient/', views.del_patient, name="delete_patient"),
    path('delete_staff/', views.del_staff, name="delete_staff"),
    path('delete_doctor/', views.del_doctor, name="delete_doctor"),
    path('delete_alert/', views.del_alert, name="delete_alert"),
    path('delete_room/', views.del_room, name="delete_room"),
    path('sign-in.html', views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout")
]
