from django.urls import path

from . import views

app_name = 'webapp'
urlpatterns = [
      path('home/', views.home, name='home'),
    path('add_appuser/', views.add_appuser_view),
    path('add_pacient/', views.add_pacient_view, name='add_pacient'),
    path('add_drug/', views.add_drug_view, name='add_drug'),
    path('search_user/', views.search_user_view, name='search_user'),
    path('get_admin/', views.get_admin_view, name='get_admin'),
    path('register/', views.register, name='register'),
]


