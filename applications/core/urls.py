from django.urls import path
from django.views.generic import RedirectView
from rest_framework.routers import SimpleRouter
from applications.core.controllers.companies_controller import CompaniesController

urlpatterns = [path('', RedirectView.as_view(url='companies'), name='home')]

router = SimpleRouter()
router.register(r'companies', CompaniesController, basename='companies')
urlpatterns += router.urls
