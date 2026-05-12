from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Teacher(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name

class Exam(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    test_code = models.CharField(max_length=20, unique=True)

    duration = models.IntegerField(help_text="Duration in Minutes")

    total_marks = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    QUESTION_TYPES = (
        ('mcq', 'MCQ'),
        ('coding', 'Coding'),
        ('descriptive', 'Descriptive'),
    )

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    question_text = models.TextField()

    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

    option1 = models.CharField(max_length=200, blank=True, null=True)
    option2 = models.CharField(max_length=200, blank=True, null=True)
    option3 = models.CharField(max_length=200, blank=True, null=True)
    option4 = models.CharField(max_length=200, blank=True, null=True)
    correct_answer = models.CharField(max_length=200, blank=True, null=True)

    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.question_text

class Student(models.Model):
    name = models.CharField(max_length=100)

    email = models.EmailField()

    university_name = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    answer = models.TextField(blank=True, null=True)

    is_correct = models.BooleanField(default=False)

    marks_obtained = models.IntegerField(default=0)

class Result(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)

    obtained_marks = models.IntegerField(default=0)

    total_marks = models.IntegerField(default=0)

    percentage = models.FloatField(default=0.0)

    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.student.name} - {self.exam.title}"