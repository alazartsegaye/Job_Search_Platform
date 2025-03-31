from django.shortcuts import render
from .models import Job, JobApplication
from .serializers import JobSerializer, JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsEmployerOrReadOnly
from rest_framework.generics import CreateAPIView, UpdateAPIView, ListAPIView
from rest_framework import filters, status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

class JobPagination(PageNumberPagination):
     # Custom pagination class for job lists, setting the page size to 10
    page_size = 10

# Manage job listings (CRUD)
class JobView(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsEmployerOrReadOnly]
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['title', 'company', 'location']
    search_fields = ['title', 'company', 'location']
    http_method_names = ['get', 'put', 'patch', 'delete']
    pagination_class = JobPagination

    def get_queryset(self):
        # Return jobs for the authenticated user if they are not staff
        if self.request.user.is_authenticated and not self.request.user.is_staff:
            return Job.objects.filter(employer=self.request.user)
        return Job.objects.all()

    def perform_update(self, serializer):
        job = self.get_object()
        # Ensure the user is the employer of the job before allowing updates
        if job.employer != self.request.user:
            raise PermissionDenied("You are not allowed to edit this job.")
        serializer.save()

# Apply for a job (authenticated users only)
class JobApplyView(CreateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        job = serializer.validated_data["job"]

        # Prevent duplicate applications
        if JobApplication.objects.filter(applicant=user, job=job).exists():
            raise PermissionDenied("You have already applied for this job.")
        
        # Prevent employer from applying to their own job
        if job.employer == user:
            raise PermissionDenied("Employers cannot apply to their own job postings.")

        serializer.save(applicant=user, status=JobApplication.Status.PENDING)

# Create a new job (authenticated users only)
class JobCreateView(CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the job with the current user as the employer
        serializer.save(employer=self.request.user)
    
# Renders job listings with optional search functionality.
def job_listings_view(request):
    query = request.GET.get('search', '')

    if query:
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        jobs = Job.objects.all()

    return render(request, 'jobs/job_listings.html', {'jobs': jobs, 'query': query})

# List job applications for the employer
class JobApplicationListView(ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrReadOnly]
    pagination_class = JobPagination

    def get_queryset(self):
        # Return job applications for jobs owned by the authenticated employer
        return JobApplication.objects.filter(job__employer=self.request.user)

# Update job application status (employer only)
class JobApplicationResponseView(UpdateAPIView):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated, IsEmployerOrReadOnly]

    def update(self, request, *args, **kwargs):
        obj = self.get_object()
        # Ensure the user is the employer of the job before allowing updates
        if obj.job.employer != request.user:
            raise PermissionDenied("You can only update applications for your own job posts.")
        
        new_status = request.data.get("status")
        obj.status = new_status
        obj.save()

        return Response(
            {"message": f"Application status updated to {obj.status}"},
            status=status.HTTP_200_OK,
        )

# Lists non-pending job applications of the authenticated user.
class ApplicantJobApplicationView(ListAPIView):
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = JobPagination

    def get_queryset(self):
        # Return job applications for the authenticated user, excluding pending applications
        return JobApplication.objects.filter(applicant=self.request.user).exclude(status=JobApplication.Status.PENDING)