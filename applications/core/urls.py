from django.urls import path
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter
from . import views


from applications.core.controllers.companies_controller import CompaniesController

urlpatterns = [path('', RedirectView.as_view(url='companies'), name='home'),
               path('sugerencia/', views.sugerencia, name='sugerencia'),
               path('contacto/', views.contacto, name='contacto'), ]

router = SimpleRouter()
router.register(r'companies', CompaniesController, basename='companies')
urlpatterns += router.urls
