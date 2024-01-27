from django.urls import path
from . import views

urlpatterns = [
    path('sugerencia/', views.sugerencia, name='sugerencia'),
    path('contacto/', views.contacto, name='contacto'),
]
