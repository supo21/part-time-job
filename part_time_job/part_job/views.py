from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import  messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import random

# Create your views here.
def home(request):
    queryset= list(job.objects.all())
    featured_jobs = random.sample(queryset, 3)
    context = {'featured_jobs': featured_jobs}
    
    return render(request, "home.html", context)

def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not User.objects.filter(username = username):
            messages.error(request, "Invalid Username.")
            return redirect("/login/")
        
        user = authenticate(username = username, password = password)

        if user is None:
            messages.error(request, "Invalid Password.")
            return redirect("/login/")
        
        else:
            login(request, user)
            return redirect("/")


    return render(request, "login.html")

def logout_page(request):
    logout(request)
    return redirect("/")

def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.filter(username= username)

        if user.exists():
            messages.info(request, "Username already taken.")
            return redirect("/register/")
        
        else:
            user = User.objects.create(
                first_name = first_name,
                last_name = last_name,
                username = username,
            )

            user.set_password(password)
            user.save()
            messages.info(request, "Account created successfully.")
            return redirect("/register/")

    return render(request, "register.html")

@login_required(login_url = "/login/")
def post_job(request):
    if request.method == "POST":
        job_name = request.POST.get("job_name")
        job_description = request.POST.get("job_description")

        job.objects.create(
            job_name = job_name,
            job_description = job_description,
        )

        return redirect("/")
    
    return render(request, "post_job.html")

def browse_jobs(request):
    
    all_jobs = job.objects.all()  
    context = {"all_jobs": all_jobs}

    return render(request, "browse_jobs.html", context)

def about_us(request):
    return render(request, "about_us.html")

def contact_us(request):
    return render(request, "contact_us.html")


