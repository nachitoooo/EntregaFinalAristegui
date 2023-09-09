from django.shortcuts import render, redirect
from .models import Blog, Profile
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CustomRegistrationForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib import messages

def home(request):
    return render(request, 'blog/home.html')

def blog_detail(request, blog_id):
    return render(request, 'blog/detail.html')


def blog_list(request):
    return render(request, 'blog/blog_list.html')


def about(request):
    return render(request, 'blog/about.html')

def profile(request):
    return render(request, 'blog/profile.html')

def create_blog(request):
    return render(request, 'blog/create_blog.html')

def update_blog(request):
    return render(request, 'blog/update_blog.html')

def album_view(request):
    return render(request, 'blog/album.html')

def about(request):
    return render(request, 'blog/about.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Credenciales inválidas. Por favor, inténtalo de nuevo.')
    else:
        form = AuthenticationForm()

    return render(request, 'blog/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            if 'profile_picture' in request.FILES:
                profile.profile_image = request.FILES['profile_picture']
                profile.save()
            return redirect('home')
    else:
        form = CustomRegistrationForm()
    return render(request, 'blog/registro.html', {'form': form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('home') 
    else:
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'blog/update_profile.html', {'profile_form': profile_form})


def user_logout(request):
    logout(request)
    return redirect('home') 


def upload_avatar(request):
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')
    else:
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
    return render(request, 'blog/home.html', {'profile_form': profile_form})

