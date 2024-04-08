<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Student, Teacher, Review
from .forms import StudentForm, TeacherForm, ReviewForm, LoginForm
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:  # Check if the user is an admin
                    return redirect('admin_dashboard')  # Redirect admin to admin dashboard
                else:
                    return redirect('student_dashboard')  # Redirect student to student dashboard
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_role = request.POST.get('user_role')  # Get the selected user role from the form
            if user_role == 'student':
                user.save()  # Save the user
                Student.objects.create(user=user)  # Create a student profile for the user
            elif user_role == 'staff':
                user.is_staff = True  # Mark the user as staff
                user.save()  # Save the user
=======
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from StudentFeedbackApp.models import Student, Teacher, Admin, Review
from StudentFeedbackApp.serializer import StudentSerializer, TeacherSerializer, AdminSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import authenticate,login
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

class CSRFTokenView(APIView):
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token})
class StudentReviewCreate(generics.CreateAPIView):
    """
    API endpoint to allow students to create reviews for existing teachers.

    Permissions:
        - IsAuthenticated: Only authenticated students can access this endpoint.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Override perform_create method to ensure the teacher exists and associate the review with the student.

        If the provided teacher ID does not exist, raise ValidationError.
        """
        teacher_id = self.request.data.get('teacher')
        teacher_exists = Teacher.objects.filter(id=teacher_id).exists()
        if not teacher_exists:
            raise serializer.ValidationError("Teacher does not exist.")
        
        student = self.request.user.student
        serializer.save(student=student)

class TeacherListCreate(generics.ListCreateAPIView):
    """
    API endpoint to list all teachers and allow admin to create new teachers.

    Permissions:
        - IsAdminUser: Only admin users can access this endpoint.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]

class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific teacher.

    Permissions:
        - IsAdminUser: Only admin users can access this endpoint.
    """
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminUser]

class ReviewList(generics.ListAPIView):
    """
    API endpoint to list all reviews and allow students and admins to view their own reviews.

    Permissions:
        - IsAuthenticated: Only authenticated users can access this endpoint.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override get_queryset method to filter reviews based on user role.

        Students can only see their own reviews, while admins can see all reviews.
        """
        user = self.request.user
        if hasattr(user, 'student'):
            return Review.objects.filter(student=user.student)
        else:
            return Review.objects.all()

class ReviewDetail(generics.RetrieveAPIView):
    """
    API endpoint to retrieve a specific review.

    Permissions:
        - IsAuthenticated: Only authenticated users can access this endpoint.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

class StudentListCreate(generics.ListCreateAPIView):
    """
    API endpoint to list all students and allow admin to create new students.

    Permissions:
        - IsAdminUser: Only admin users can access this endpoint.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint to retrieve, update, or delete a specific student.

    Permissions:
        - IsAdminUser: Only admin users can access this endpoint.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsAdminUser]

class UserLogin(APIView):
    """
    API endpoint to log in users.

    Permissions:
        - AllowAny: Anyone can access this endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Override post method to authenticate user login.

        If credentials are valid, log in user; otherwise, return error message.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
>>>>>>> 51c909ada6ff0ba4f73337b943b67ca149b3ea87
            login(request, user)
            return redirect('homepage')  # Redirect to homepage after signup
    else:
        form = StudentForm()
    return render(request, 'signup.html', {'form': form})

<<<<<<< HEAD
@login_required
def create_review(request, teacher_id):
    teacher = get_object_or_404(Teacher, pk=teacher_id)
=======

@method_decorator(csrf_exempt, name='dispatch')
class UserSignup(APIView):
    """
    API endpoint to sign up new students.
>>>>>>> 51c909ada6ff0ba4f73337b943b67ca149b3ea87

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.teacher = teacher
            review.student = request.user.student
            review.save()
            return redirect('teacher_detail', pk=teacher_id)
    else:
        form = ReviewForm()

    return render(request, 'create_review.html', {'form': form, 'teacher': teacher})

<<<<<<< HEAD
@login_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_manage')  # Redirect to teacher management page after creating teacher
    else:
        form = TeacherForm()
    return render(request, 'create_teacher.html', {'form': form})

@login_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect('teacher_manage')  # Redirect to teacher management page after deleting teacher

@login_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_manage')  # Redirect to student management page after creating student
    else:
        form = StudentForm()
    return render(request, 'create_student.html', {'form': form})

@login_required
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_manage')  # Redirect to student management page after deleting student

@login_required
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'review_list.html', {'reviews': reviews})

def teacher_manage(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_manage.html', {'teachers': teachers})

def student_manage(request):
    students = Student.objects.all()
    return render(request, 'student_manage.html', {'students': students})

def student_reviews(request):
    student = request.user.student
    reviews = Review.objects.filter(student=student)
    return render(request, 'student_reviews.html', {'reviews': reviews})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

def homepage(request):
    return render(request, 'index.html')
=======
        If provided data is valid, create a new student; otherwise, return error message.
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 51c909ada6ff0ba4f73337b943b67ca149b3ea87
