from django.urls import path
from . import views

urlpatterns = [
    path('sugerencia/', views.send_suggestion, name='send_suggestion'),
]
