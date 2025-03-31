from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['posted_at', 'employer']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'email', 'cover_letter', 'resume', 'applied_at', 'status']
        read_only_fields = ["applied_at", "status"]

    def create(self, validated_data):

        validated_data.pop("status", None)
        return super().create(validated_data)