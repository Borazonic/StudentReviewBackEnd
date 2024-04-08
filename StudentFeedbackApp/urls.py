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
from StudentFeedbackApp.views import CSRFTokenView,StudentReviewCreate,TeacherListCreate,TeacherDetail,StudentDetail,StudentListCreate,ReviewList,ReviewDetail,UserLogin,UserSignup
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('student-review/', StudentReviewCreate.as_view(), name='student-review-create'),
    path('teachers/', TeacherListCreate.as_view(), name='teacher-list-create'),
    path('teachers/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),
    path('students/<int:pk>/', StudentDetail.as_view(), name='student-detail'),
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('reviews/', ReviewList.as_view(), name='review-list'),
    path('reviews/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('signup/', UserSignup.as_view(), name='user-signup'),
    path('get-csrf-token/', CSRFTokenView.as_view(), name='get_csrf_token'),
]

