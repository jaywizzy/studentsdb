from rest_framework import serializers
from .models import Students

class StudentsSerializer(serializers.ModelSerializer):
    model = Students
    fields = '__all__'