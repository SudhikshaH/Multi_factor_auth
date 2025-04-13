from django.shortcuts import render, redirect
from django.contrib import messages
<<<<<<< HEAD
from django.contrib.auth import login
from .models import UserDetails
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
=======
from .models import UserDetails
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken
>>>>>>> origin/master
from deepface import DeepFace
from PIL import Image
from tempfile import NamedTemporaryFile
import os
    
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
<<<<<<< HEAD
        password = make_password(request.POST['password'])
=======
        password = request.POST['password']
>>>>>>> origin/master
        email = request.POST.get('email')
            
        if UserDetails.objects.filter(name=name).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')
<<<<<<< HEAD

        user = UserDetails(name=name, password=password, email=email)
        user.save()
        request.session['user_email']=email
        return redirect('signup_camera')
    return render(request,'index.html',{"authentication_type":"signup"})

=======
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


>>>>>>> origin/master
def signup_camera(request):
    if request.method == "POST":
        email = request.session.get('user_email')
        captured_image = request.FILES.get('face-image',None)
        try:
            user = UserDetails.objects.get(email=email)
<<<<<<< HEAD
            user.image.save(f"{user.name}_image.jpg", captured_image)
=======
            user.image.save(f"{user.name}_image.png", captured_image)
>>>>>>> origin/master
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
<<<<<<< HEAD
        if not email:
            return JsonResponse({"message": "No email found in session"})
        
        if not captured_image:
            return JsonResponse({"message": "No image captured"})
        
        try:
            user = UserDetails.objects.get(email=email)
            stored_image_path=user.image.path
            if not os.path.exists(stored_image_path):
                raise FileNotFoundError(f"stored image path '{stored_image_path}' does not exist.")
            print(f"Stored image path: {stored_image_path}")


            with NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                image = Image.open(captured_image)
                if image.mode != "RGB":
                    image = image.convert("RGB")  # Ensure the image is in RGB mode
                image.save(temp_file, format="JPEG")
                temp_file_path=temp_file.name
                if not os.path.exists(temp_file_path):
                    print(f"Temporary file created at: {temp_file_path}")

            if not os.path.exists(temp_file_path) or os.path.getsize(temp_file_path) < 100:
                raise ValueError("Captured image file is missing or invalid.")

            result=DeepFace.verify(temp_file_path, stored_image_path)
            #print(result)
            os.remove(temp_file_path)
            if result.get('verified'):
                return redirect('home')
            else:
                JsonResponse({"message":"Authentication failed. Please adjust your camera."})
                return redirect('signin')
        except Exception as e:
            print("Exception during DeepFace processing:", e)
            if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
                os.remove(temp_file_path)
                print("Temporary file removed during exception handling.")
            return JsonResponse({"message": f"An error occurred: {str(e)}"})
    return render(request,'signin_camera.html')
        
def home(request):
    return render(request, 'home.html')
=======
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
>>>>>>> origin/master
