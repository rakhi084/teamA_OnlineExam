from django.contrib import admin
from .models import (
    Teacher,
    Exam,
    Question,
    Student,
    StudentAnswer,
    Result
)

admin.site.register(Teacher)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Student)
admin.site.register(StudentAnswer)
admin.site.register(Result)