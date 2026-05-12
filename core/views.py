from django.shortcuts import render, redirect
from .models import *
import random
import string
from django.shortcuts import get_object_or_404

# Create your views here.
def home(request):
    return render(request, 'core/home.html')

def signup(request):

    if request.method == "POST":

        full_name = request.POST.get('full_name')

        email = request.POST.get('email')

        institution = request.POST.get('institution')

        password = request.POST.get('password')

        confirm_password = request.POST.get('confirm_password')

        # PASSWORD MATCH CHECK
        if password != confirm_password:

            return render(request, 'signup.html', {
                'error': 'Passwords do not match'
            })
        # SAVE DATA
        Teacher.objects.create(
            full_name=full_name,
            email=email,
            institution=institution,
            password=password
        )

        return redirect('teacher_login')

    return render(request, 'core/signup.html')

# TEACHER LOGIN
def teacher_login(request):

    error = None

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        teacher = Teacher.objects.filter(
            email=email,
            password=password
        ).first()

        if teacher:
             # STORE TEACHER ID IN SESSION
            request.session['teacher_id'] = teacher.id

            return redirect('teacher_dashboard')

        else:
            error = "Invalid email or password"

    return render(request, 'core/teacher_login.html', {
        'error': error
    })

def teacher_dashboard(request):

    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('teacher_login')

    teacher = Teacher.objects.get(id=teacher_id)

    exams = Exam.objects.filter(
        teacher=teacher
    ).order_by('-created_at')

    for exam in exams:

        exam.question_count = Question.objects.filter(
            exam=exam
        ).count()
    context = {

        'exams': exams,

        'total_exams': exams.count(),

        'total_questions': Question.objects.filter(
            exam__teacher=teacher
        ).count(),

        'total_results': Result.objects.filter(
            exam__teacher=teacher
        ).count(),
    }
    return render(
        request,
        'core/teacher_dashboard.html',
        context
    )


# CREATE TEST
def create_test(request):

    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('teacher_login')

    teacher = Teacher.objects.get(id=teacher_id)

    if request.method == 'POST':

        title = request.POST.get('title')
        description = request.POST.get('description')
        duration = request.POST.get('duration')

        # AUTO GENERATE TEST CODE
        test_code = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6 
                )
        )

        exam = Exam.objects.create(
            teacher=teacher,   # IMPORTANT
            title=title,
            description=description,
            duration=duration,
            test_code=test_code
        )

        return redirect('add_questions', exam.id)

    return render(request, 'core/create_test.html')

# STUDENTS
def students(request):

    return render(request, 'core/students.html')


# RESULTS
def results(request):

    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('teacher_login')

    teacher = Teacher.objects.get(id=teacher_id)

    all_results = Result.objects.filter(
        exam__teacher=teacher
    ).select_related(
        'student',
        'exam'
    ).order_by('-submitted_at')
    return render(
        request,
        'core/results.html',
        {
            'results': all_results
        }
    )


def student_access(request):

    if request.method == "POST":

        student_key = request.POST.get('student_key')

        exam = Exam.objects.filter(test_code=student_key).first()

        if exam:

            return render(request, 'core/student_exam.html', {
                'exam': exam
            })

        return render(request, 'core/home.html', {
            'error': 'Invalid Test Code'
        })

    return redirect('home')

from .models import Exam


def start_exam(request, exam_id):

    exam = Exam.objects.get(id=exam_id)

    questions = Question.objects.filter(exam=exam)

    return render(request, 'core/start_exam.html', {
        'exam': exam,
        'questions': questions
    })

def add_questions(request, exam_id):

    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':

        question_text = request.POST.get('question_text')

        option1 = request.POST.get('option1')
        option2 = request.POST.get('option2')
        option3 = request.POST.get('option3')
        option4 = request.POST.get('option4')

        correct_answer = request.POST.get('correct_answer')

        marks = request.POST.get('marks')

        Question.objects.create(
            exam=exam,
            question_text=question_text,
            question_type='mcq',

            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,

            correct_answer=correct_answer,
            marks=marks
        )

        return redirect('add_questions', exam.id)

    questions = Question.objects.filter(exam=exam)

    return render(request, 'core/add_questions.html', {
        'exam': exam,
        'questions': questions
    })

def submit_exam(request, exam_id):

    exam = get_object_or_404(Exam, id=exam_id)

    student_id = request.session.get('student_id')

    student = Student.objects.get(id=student_id)

    questions = Question.objects.filter(exam=exam)

    total_marks = 0
    obtained_marks = 0
    for question in questions:

        total_marks += question.marks

        answer = request.POST.get(f'question_{question.id}')

        is_correct = False
        marks_obtained = 0

        if question.question_type == 'mcq':

            if answer == question.correct_answer:

                is_correct = True

                marks_obtained = question.marks

                obtained_marks += marks_obtained

        StudentAnswer.objects.create(
            student=student,
            exam=exam,
            question=question,
            answer=answer,
            is_correct=is_correct,
            marks_obtained=marks_obtained
        )

    percentage = 0

    if total_marks > 0:

        percentage = (obtained_marks / total_marks) * 100

    Result.objects.create(
        student=student,
        exam=exam,
        obtained_marks=obtained_marks,
        total_marks=total_marks,
        percentage=percentage
    )

    return render(request, 'core/student_result.html', {
        'student': student,
        'exam': exam,
        'obtained_marks': obtained_marks,
        'total_marks': total_marks,
        'percentage': round(percentage, 2)
    })
    
def student_details(request, exam_id):

    exam = get_object_or_404(Exam, id=exam_id)

    if request.method == 'POST':

        student = Student.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            university_name=request.POST.get('university_name')
        )

        request.session['student_id'] = student.id

        return redirect('start_exam', exam.id)

    return render(request, 'core/student_details.html', {
        'exam': exam
    })

def start_exam(request, exam_id):

    exam = get_object_or_404(Exam, id=exam_id)

    questions = Question.objects.filter(exam=exam)

    return render(request, 'core/start_exam.html', {
        'exam': exam,
        'questions': questions
    })

def delete_exam(request, exam_id):

    teacher_id = request.session.get('teacher_id')

    if not teacher_id:
        return redirect('teacher_login')

    exam = get_object_or_404(
        Exam,
        id=exam_id,
        teacher_id=teacher_id
    )

    exam.delete()

    return redirect('teacher_dashboard')