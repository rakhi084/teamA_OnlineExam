from django.urls import path
from . import views

urlpatterns = [

    path('signup/', views.signup, name='signup'),
    path(
    'teacher-dashboard/',
    views.teacher_dashboard,
    name='teacher_dashboard'
),
path(
    'delete-exam/<int:exam_id>/',
    views.delete_exam,
    name='delete_exam'
),

]