from django.urls import path

from . import views

app_name = 'webapp'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('add_profile/', views.add_profile_view, name='add_profile'),
    path('add_pacient/', views.add_pacient_view, name='add_pacient'),
    path('add_drug/', views.add_drug_view, name='add_drug'),
    path('add_exam/', views.add_exam_view, name='add_exam'),
    path('add_prescription/', views.add_prescription_view, name='add_prescription'),
    path('add_appointment/', views.add_appointment_view, name='add_appointment'),
    path('search_user/', views.search_user_view, name='search_user'),
    path('search_pacient/', views.search_pacient_view, name='search_pacient'),
    path('search_drug/', views.search_drug_view, name='search_drug'),
    path('search_appointment/', views.search_appointment_view, name='search_appointment'),
    path('search_prescription/', views.search_prescription_view, name='search_prescription'),
    path('search_exam/', views.search_exam_view, name='search_exam'),
]


