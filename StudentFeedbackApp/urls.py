from django.urls import path
from . import views

urlpatterns = [
    path('students/', views.StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:pk>/', views.StudentDetail.as_view(), name='student-detail'),
    path('teachers/', views.TeacherListCreate.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', views.TeacherDetail.as_view(), name='teacher-detail'),
    path('reviews/', views.ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', views.ReviewDetail.as_view(), name='review-detail'),
]
