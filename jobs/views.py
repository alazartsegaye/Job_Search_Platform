from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, permissions, generics
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from django.contrib.auth.decorators import login_required

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-posted_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

@login_required
class ApplyJobView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job = get_object_or_404(Job, id=self.kwargs['job_id'])
        serializer.save(applicant=self.request.user, job=job)

class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

class JobApplicationListView(generics.ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        job = get_object_or_404(Job, id=self.kwargs['job_id'])
        return JobApplication.objects.filter(job=job)


def job_listings_view(request):
    jobs = Job.objects.all().order_by('-posted_at')
    return render(request, 'jobs/job_listings.html', {'jobs': jobs})