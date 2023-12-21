from rest_framework.serializers import ModelSerializer

from applications.tenants.models import Organization


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
