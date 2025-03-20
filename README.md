# JobSearch API

JobSearch API is a Django-based job board API that allows users to post, apply for, and manage job listings. The API provides authentication, user management, job applications, and role-based permissions.

---

## Features

- **User Authentication** (Register, Login, Logout)
- **Role-based Access Control**
  - Employers can **create, update, and delete** job posts.
  - Applicants can **apply** for jobs and **view application status**.
  - Employers can **view and manage job applications**.
- **Job Search and Filtering**
- **API Endpoints for Job Listings & Applications**
- **Admin Panel for Managing Users and Jobs**

---

## Technologies Used

- **Django** & **Django REST Framework (DRF)**
- **MySQL** as the database
- **Session-Based Authentication**
- **PythonAnywhere Deployment**
- **HTML Templates for Authentication**
- **HTML Templates for Job Lists**

---

## Project Structure

Job_search_Platform/
├── job_search_api/          # Project configuration
│   ├── __init__.py          
│   ├── asgi.py              # ASGI configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│
├── jobs/                    # Jobs app
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Job & Application models
│   ├── permissions.py       # Permissions for job-related actions
│   ├── serializers.py       # Serializers for API responses
│   ├── tests.py             # Unit tests for jobs app
│   ├── urls.py              # URL routing for jobs
│   ├── views.py             # View logic (CBV & FBV)
│
├── users/                   # Users app
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Custom user model
│   ├── permissions.py       # User permissions
│   ├── serializers.py       # Serializers for users
│   ├── tests.py             # Unit tests for users app
│   ├── urls.py              # URL routing for users
│   ├── views.py             # Authentication & profile management
│
├── static/                  # Static files (CSS, JavaScript, images)
│   ├── css/                 # Stylesheets
│   ├── images/              # Image assets
│
├── templates/               # HTML templates (for authentication & admin)
|   ├── base.html 
│   ├── users/
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── register.html
│   ├── jobs/
│   │   ├── job_listings.html
|
├── manage.py                # Django command-line utility
├── requirements.txt         # Project dependencies
├── README.md                # Project documentation
└── .gitignore               # Git ignored files
