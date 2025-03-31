from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (JobView, JobApplyView, job_listings_view, JobApplicationListView, JobCreateView,
                    JobApplicationResponseView, ApplicantJobApplicationView )

router = DefaultRouter()
router.register(r'jobs', JobView, basename='job')

urlpatterns = [

    path('', include(router.urls)),
    path('job/lists/', job_listings_view, name='job_listings'),
    path('job/create/', JobCreateView.as_view(), name='job-create'),
    path('job/apply/', JobApplyView.as_view(), name='apply_job'),
    path('job/application/', JobApplicationListView.as_view(), name='employer-applications'),
    path('application/<int:pk>/respond/', JobApplicationResponseView.as_view(), name='respond-application'),
    path('applicant/application/', ApplicantJobApplicationView.as_view(), name='applicant-applications'),
]
