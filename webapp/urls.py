from django.urls import path

from . import views

app_name = 'webapp'
urlpatterns = [
    path('auth/', views.auth),
    path('home/', views.home, name='home'),
    path('add_appuser/', views.add_appuser_view),
    path('register/', views.register, name='register'),
]


