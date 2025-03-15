from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, generics
from .models import Job
from .serializers import JobSerializer, JobApplicationSerializer
from django.http import JsonResponse
from django.views import View
from rest_framework import filters

class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all().order_by('-posted_at')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'company__name', 'location']


    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

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


class JobDetailView(View):
    def get(self, job_id):
        try:
            job = Job.objects.get(id=id)
            data = {
                'id': job.id,
                'title': job.title,
                'description': job.description,
            }
            return JsonResponse(data)
        except Job.DoesNotExist:
            return JsonResponse({'error': 'Job not found'}, status=404)

def job_listings_view(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_listings.html', {'jobs': jobs})