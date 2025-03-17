from django.shortcuts import render, get_object_or_404
from .serializers import JobSerializer, JobApplicationSerializer
from .models import Job
from rest_framework import viewsets, permissions, generics
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-posted_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['title', 'company', 'location']


    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

class ApplyJobView(generics.CreateAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        job = get_object_or_404(Job, id=self.kwargs['job_id'])
        serializer.save(applicant=self.request.user, job=job)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response(
                {"detail": "Authentication required. Please log in or create an account to apply for this job."},
                status=403
            )
        return super().handle_exception(exc)

class JobCreateView(generics.CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

def job_listings_view(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_listings.html', {'jobs': jobs})