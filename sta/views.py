from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import login, logout,authenticate
from sta.admin import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserImageForm
from .models import ImageUpload
from django.db.models import Q


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congratulations.. Registration done')
            user = form.save()
            form = UserCreationForm()        
    else:
        form = UserCreationForm()
    return render(request, 'sta/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        # If the user is already logged in, redirect to the dashboard
        return redirect('dashboard')

    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            
            else:
                messages.error(request,"Invalid email or password")
                
        else:
                messages.error(request,"Invalid email or password")
            
    return render(request, 'sta/login.html',context={'form':AuthenticationForm()})


def home(request):
    return render(request, 'sta/home.html')

@login_required(login_url='/')  
def dashboard(request):
    user = request.user

    if not user.is_authenticated:
        # If the user is not authenticated, redirect to the login page
        return redirect('login_view')

    if user.user_type == 'admin':
        # Admin dashboard: Display all images uploaded by teacher and student, ordered by latest
        all_images = ImageUpload.objects.all().order_by('-created_at')
        context = {'user_type': 'admin', 'images': all_images}

    elif user.user_type == 'student':
        # Student dashboard: Display only self images
        user_images = ImageUpload.objects.filter(user=user).order_by('-created_at')
        context = {'user_type': 'student', 'images': user_images}

    elif user.user_type == 'teacher':
        # Teacher dashboard: Display only self images and student images
        user_and_student_images = ImageUpload.objects.filter(
        Q(user=user) | Q(user__user_type='student')
        ).order_by('-created_at')
        context = {'user_type': 'teacher', 'images': user_and_student_images}

    else:
        # Handle other user types or unknown types
        return redirect('login_view')

    return render(request, 'sta/dashboard.html', context)
@login_required(login_url='/')  
def upload_image(request):
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            user_image.user = request.user
            user_image.save()
            return redirect('dashboard')  
    else:
        form = UserImageForm()

    return render(request, 'sta/upload_image.html', {'form': form})
    
def logout_view(request):
    logout(request)
    return redirect('home')
