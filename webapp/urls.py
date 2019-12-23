from django.urls import path

from . import views

app_name = 'webapp'
urlpatterns = [
    path('add_appuser/', views.add_appuser_view)
]


