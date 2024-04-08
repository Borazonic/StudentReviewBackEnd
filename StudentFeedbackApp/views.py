from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from StudentFeedbackApp.models import Student, Teacher, Admin, Review
from StudentFeedbackApp.serializer import StudentSerializer, TeacherSerializer, AdminSerializer, ReviewSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.contrib.auth import authenticate,login,logout

@api_view(['GET'])
def get_csrf_token(request):
    """
    API endpoint to get CSRF token.

    Permissions:
        - AllowAny: Anyone can access this endpoint.
    """
    csrf_token = csrf.get_token(request)
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
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserSignup(APIView):
    """
    API endpoint to sign up new students.

    Permissions:
        - AllowAny: Anyone can access this endpoint.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Override post method to register new students.

        If provided data is valid, create a new student; otherwise, return error message.
        """
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserLogout(APIView):
    """
    API endpoint to log out users.

    Permissions:
        - IsAuthenticated: Only authenticated users can access this endpoint.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Override post method to log out user.

        Logs out the currently authenticated user.
        """
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)