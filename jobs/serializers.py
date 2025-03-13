from rest_framework import serializers
from .models import Job, JobApplication

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'title', 'description', 'company', 'location', 'posted_at']
        read_only_fields = ['posted_at', 'posted_by']

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'applicant', 'applied_at', 'cover_letter', 'resume']
        read_only_fields = ['applied_at', 'applicant']

