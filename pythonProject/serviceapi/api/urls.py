from django.urls import path

from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [path('doctors/', views.doctors),
path('patients/', views.patients),
path('staff/', views.staff),
path('users/', views.users),
path('doctor/', views.doctor),
path('patient/', views.patient),
path('staff/', views.staff),
path('user/', views.user),
path('add_user/', views.add_user),
path('add_patient/', views.add_patient),
path('add_staff/', views.add_staff),
path('add_doctor/', views.add_doctor),


path('edit_user/', views.ed_user),
path('edit_patient/', views.ed_patient),
path('edit_staff/', views.ed_staff),
path('edit_doctor/', views.ed_doctor),

# path('delete_user/', views.del_user),
# path('delete_patient/', views.del_patient),
# path('delete_staff/', views.del_staff),
# path('delete_doctor/', views.del_doctor)


]
