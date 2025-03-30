# JOB SEARCH PLATFORM API

A full-featured job management platform built with Django that connects employers and job seekers. This application allows employers to post jobs and manage applications while job seekers can search for and apply to positions.

## Features

### User Management
- Custom User model extending Django's AbstractUser
- Role-based functionality (employer/applicant)
- User registration and authentication with token support
- Profile management

### For Employers
- Create and manage job listings
- View and respond to applications
- Track applicant status

### For Job Seekers
- Browse and search job listings
- Apply to jobs with resume and cover letter
- Track application status

### API
- RESTful API with token authentication
- Comprehensive permissions system
- Endpoints for users, jobs, and applications

## Technology Stack

- **Backend**: Django 4.2, Django REST Framework
- **Database**: MySQL (development), MySQL (production-ready)
- **Authentication**: Django Authentication, Token Authentication
- **Environment Management**: python-dotenv

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/django-job-management.git
   cd JOB_Search_Platform
