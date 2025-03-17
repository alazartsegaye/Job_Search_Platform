from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobViewSet, ApplyJobView, JobCreateView, job_listings_view

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')

urlpatterns = [

    path('', include(router.urls)),
    path('listings/', job_listings_view, name='job_listings'),
    path('create/', JobCreateView.as_view(), name='create_job'),
    path('<int:job_id>/apply/', ApplyJobView.as_view(), name='apply_job'),
]