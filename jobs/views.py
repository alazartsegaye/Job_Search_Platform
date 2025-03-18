from django.shortcuts import render
from .serializers import JobSerializer, JobApplicationSerializer
from .models import Job, JobApplication
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, filters
from rest_framework import permissions
from .permissions import IsEmployer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

class JobListView(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['title', 'company', 'location']

class JobDetailView(RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'id'

class JobApplyView(CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise PermissionDenied("You must be logged in to apply for a job.")
        serializer.save(applicant=self.request.user)

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            return Response({"detail": str(exc)}, status=403)
        return super().handle_exception(exc)

class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(employer=self.request.user)

class JobUpdateView(UpdateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated, IsEmployer]
    lookup_field = 'id'

    def perform_update(self, serializer):
        serializer.save(employer=self.request.user)

class JobDeleteView(DestroyAPIView):
    queryset = Job.objects.all()
    permission_classes = [IsAuthenticated, IsEmployer]
    lookup_field = 'id'

def job_listings_view(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_listings.html', {'jobs': jobs})