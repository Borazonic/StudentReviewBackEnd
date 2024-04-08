"""
URL configuration for SWEBackend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from StudentFeedbackApp.views import StudentReviewCreate,TeacherListCreate,TeacherDetail,StudentDetail,StudentListCreate,ReviewList,ReviewDetail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('StudentFeedbackApp.urls')),
    path('api-auth/', include('rest_framework.urls')), 
    path('student-review-create/', StudentReviewCreate.as_view(), name='student-review-create'),  # Fixed naming convention and removed redundant comma
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'),
    path('teachers/', TeacherListCreate.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
]