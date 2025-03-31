from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from rest_framework import status
from .models import Job, JobApplication
from rest_framework.authtoken.models import Token
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

User = get_user_model()

class JobTests(APITestCase):
    def setUp(self):
        # Create an employer user and generate an authentication token for API requests
        self.employer = User.objects.create_user(username='employer', password='password')
        self.token = Token.objects.create(user=self.employer)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)  # Set authorization header

        # Define job data for creating a job
        self.job_data = {
            "title": "Software Engineer",
            "description": "Develop software solutions.",
            "skills_required": "Python, Django",
            "company": "TechCorp",
            "location": "Remote"
        }
        
        # Create a job instance for testing
        self.job = Job.objects.create(employer=self.employer, **self.job_data)

    def test_create_job(self):
        # Test creating a new job and verify the response and job count
        response = self.client.post('/api/job/create/', self.job_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check for successful creation
        self.assertEqual(Job.objects.count(), 2)  # Verify that the job count has increased by 1
    
class JobApplyViewTests(APITestCase):
    def setUp(self):
        # Create a user and an employer for testing job applications
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.employer = User.objects.create_user(username='employer', password='employerpass')
        self.job = Job.objects.create(title='Test Job', company='Test Company', employer=self.employer)

    def test_apply_for_job_authenticated(self):
        # Test applying for a job as an authenticated user
        self.client.login(username='testuser', password='testpass')  # Log in the test user
        resume_file = SimpleUploadedFile("resume.pdf", b"Dummy resume content", content_type="application/pdf")  # Create a dummy resume file

        # Define application data for the job application
        application_data = {
            "job": self.job.id,
            "email": "applicant@example.com",
            "cover_letter": "I am very interested in this position.",
            "resume": resume_file
        }
        # Submit the job application and check the response
        response = self.client.post('/api/job/apply/', application_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Check for successful application
        self.assertEqual(JobApplication.objects.count(), 1)  # Verify that the application count has increased by 1