from django.urls import path

from . import views

app_name = 'webapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('add_profile/', views.add_profile_view, name='add_profile'),
    path('add_pacient/', views.add_pacient_view, name='add_pacient'),
    path('add_drug/', views.add_drug_view, name='add_drug'),
    path('add_exam/', views.add_exam_view, name='add_exam'),
    path('add_appointment/', views.add_appointment_view, name='add_appointment'),
    path('search_user/', views.search_user_view, name='search_user'),
]


