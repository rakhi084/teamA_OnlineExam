"""
URL configuration for exam_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import home, signup , teacher_login
from core import views

urlpatterns = [

    # ADMIN
    path('admin/', admin.site.urls),

    # HOME
    path('', views.home, name='home'),

    # AUTH
    path('signup/', views.signup, name='signup'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),

    # TEACHER DASHBOARD
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    # EXAM MODULES
    path('create-test/', views.create_test, name='create_test'),

    # path('manage-tests/', views.manage_tests, name='manage_tests'),
    path('students/', views.students, name='students'),

    path('results/', views.results, name='results'),

    path('student-access/', views.student_access, name='student_access'),

    path('start-exam/<int:exam_id>/', views.start_exam, name='start_exam'),
    path(
    'submit-exam/<int:exam_id>/',
    views.submit_exam,
    name='submit_exam'
),
path(
    'add-questions/<int:exam_id>/',
    views.add_questions,
    name='add_questions'
),
path(
    'student-details/<int:exam_id>/',
    views.student_details,
    name='student_details'
),
path(
    'delete-exam/<int:exam_id>/',
    views.delete_exam,
    name='delete_exam'
),
]
