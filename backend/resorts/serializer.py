from rest_framework import serializers

from .models import SkiPass, Resort, Conditions

class ResortSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Resort
        fields = ('url', 'name')
