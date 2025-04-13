from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from .models import UserDetails
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from deepface import DeepFace
from PIL import Image
from tempfile import NamedTemporaryFile
import os
    
def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        password = make_password(request.POST['password'])
        email = request.POST.get('email')
            
        if UserDetails.objects.filter(name=name).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')
        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        user = UserDetails(name=name, password=password, email=email)
        user.save()
        request.session['user_email']=email
        return redirect('signup_camera')
    return render(request,'index.html',{"authentication_type":"signup"})

def signup_camera(request):
    if request.method == "POST":
        email = request.session.get('user_email')
        captured_image = request.FILES.get('face-image',None)
        try:
            user = UserDetails.objects.get(email=email)
            user.image.save(f"{user.name}_image.jpg", captured_image)
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