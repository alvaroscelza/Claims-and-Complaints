from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from applications.core.serializers.companies_serializer import CompanySerializer


class CompaniesController(GenericViewSet):
    serializer_class = CompanySerializer
    queryset = serializer_class.Meta.model.objects.all()

    def list(self, _):
        companies = self.get_queryset()
        return Response({'companies': companies}, template_name='list.html')
