from abc import ABC

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class ReadableWritableModelView(viewsets.ModelViewSet, ABC):
    permission_classes = [IsAuthenticated]
    writable_serializer = None
    readable_serializer = None

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return self.readable_serializer
        return self.writable_serializer
