from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.tenants.serializers.organizations_serializers import OrganizationSerializer


class OrganizationsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer
    queryset = serializer_class.Meta.model.objects.all()

    @action(detail=False, permission_classes=[])
    def exists(self, request):
        name = request.query_params.get('name')
        exists = self.get_queryset().filter(schema_name=name).exists()
        return Response({'exists': exists})
