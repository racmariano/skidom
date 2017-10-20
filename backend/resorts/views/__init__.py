from resorts_table import resorts_table

from rest_framework import viewsets

from ..models import Resort
from ..serializer import ResortSerializer

class ResortViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Resort.objects.all()
    serializer_class = ResortSerializer