from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserDetails
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
from deepface import DeepFace
from PIL import Image
from tempfile import NamedTemporaryFile
import os
    
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        email = request.POST.get('email')
            
        if UserDetails.objects.filter(name=name).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')
        is_valid, message = valid_password(password)
        if not is_valid:
            messages.error(request, message)
            return redirect('signup')
        h_password=make_password(password)
        user = UserDetails(name=name, password=password, email=email)
        user.save()
        refresh = RefreshToken.for_user(user)
        request.session['user_email']=email
        JsonResponse({
            "message": "Signup successful!",
            "token": {
                "refresh": str(refresh),
               "access": str(refresh.access_token),
            },
        })
        return redirect('signup_camera')
    return render(request,'index.html',{"authentication_type":"signup"})


def signup_camera(request):
    if request.method == "POST":
        email = request.session.get('user_email')
        captured_image = request.FILES.get('face-image',None)
        try:
            user = UserDetails.objects.get(email=email)
            user.image.save(f"{user.name}_image.png", captured_image)
            user.save()
            #return JsonResponse({"message": "Image saved successfully!"})
            return redirect(signin)
        except UserDetails.DoesNotExist:
            return JsonResponse({"message": "User not found."})
    return render(request, 'signup_camera.html')

def signin(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST['password']
        try:
            user = UserDetails.objects.get(email=email)
            if check_password(password,user.password):
                request.session['user_email']=email
                return redirect('signin_camera')
            else:
                messages.error(request, "Incorrect email or password")
        except UserDetails.DoesNotExist:
            messages.error(request, "User not found")            
    return render(request, 'index.html',{"authentication_type":"signin"})

def signin_camera(request):
    if request.method == "POST":
        email = request.session.get('user_email')
        captured_image = request.FILES.get('face-image')
        try:
            user = UserDetails.objects.get(email=email)
            stored_image_path=user.image.path
            with NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(captured_image.read())
                temp_file_path=temp_file.name
            result=DeepFace.verify(temp_file_path, stored_image_path)
            os.remove(temp_file_path)
            if result.get('verified'):
                refresh = RefreshToken.for_user(user)
                JsonResponse({
                    "message": "Authentication successful!",
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                })
                return redirect('home')
            else:
                return redirect('error')
        except Exception as e:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            return redirect('error')
    return render(request,'signin_camera.html')
        
def home(request):
    return render(request, 'home.html')
def error(request):
    return render(request, 'error.html')

def valid_password(password):
    if len(password) < 8:
        return False,"Password must be at least 8 characters long."
    has_uppercase = False
    for char in password:
        if 'A' <= char <= 'Z':
            has_uppercase = True
            break
    if not has_uppercase:
        return False,"Password must contain at least one uppercase letter."
    has_number = False
    for char in password:
        if '0' <= char <= '9': 
            has_number = True
            break
    if not has_number:
        return False ,"Password must contain at least one number."
    special_characters = "!@#$%^&*()-_+=<>?/{}[]|"
    has_special_char = False
    for char in password:
        if char in special_characters:
            has_special_char = True
            break
    if not has_special_char:
        return False,"Password must contain at least one special character."
    return True