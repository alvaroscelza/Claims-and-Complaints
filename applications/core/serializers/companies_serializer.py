from rest_framework.serializers import ModelSerializer

from applications.core.models import Company


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
