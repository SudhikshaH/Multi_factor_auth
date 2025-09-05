from . import views
from django.urls import path

urlpatterns = [
    path('signin/',views.signin,name='signin'),
    path('signup/', views.signup, name='signup'), 
    path('signup_camera/', views.signup_camera, name='signup_camera'), 
    path('signin_camera/', views.signin_camera, name='signin_camera'),  
    path('home/', views.home, name='home
    path('error/',views.error,name='error'), 
]
