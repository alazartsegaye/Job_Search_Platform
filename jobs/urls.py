from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (JobListView, JobDetailView, JobCreateView, JobUpdateView, JobDeleteView, JobApplyView, job_listings_view)

router = DefaultRouter()
router.register(r'jobs', JobListView, basename='job')

urlpatterns = [

    path('', include(router.urls)),
    path('job/lists/', job_listings_view, name='job_listings'),
    path('job/<int:id>/', JobDetailView.as_view(), name='job-detail'),
    path('job/create/', JobCreateView.as_view(), name='create_job'),
    path('job/<int:id>/update/', JobUpdateView.as_view(), name='job-update'),
    path('job/<int:id>/delete/', JobDeleteView.as_view(), name='job-delete'),
    path('job/<int:id>/apply/', JobApplyView.as_view(), name='apply_job'),
]
