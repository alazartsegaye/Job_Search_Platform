from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills_required = models.TextField()
    company = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.title

class JobApplication(models.Model):

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')

    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"