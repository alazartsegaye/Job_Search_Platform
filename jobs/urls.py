from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplyJobView, JobCreateView, job_listings_view, JobDetailView

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
    path('listings/', job_listings_view, name='job_listings'),
    path('create/', JobCreateView.as_view(), name='create_job'),
    path('apply/<int:job_id>/', ApplyJobView.as_view(), name='apply_job'),
    path('jobs/<int:job_id>/', JobDetailView.as_view(), name='job_detail'),
]