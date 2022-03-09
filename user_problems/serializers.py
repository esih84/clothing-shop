from rest_framework import serializers
from .models import profiles


class profileserializers(serializers.ModelSerializer):
    class Meta:
        model = profiles
        fields = ['first_name', 'last_name', 'desc', 'phone', 'postal_address', 'address']

