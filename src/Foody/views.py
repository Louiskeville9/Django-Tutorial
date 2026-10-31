import pathlib
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from visits.models import PageVisit # Import custom page visit module

this_dir = pathlib.Path(__file__).resolve().parent  # Find (resolve) the parent directory

def home_page_view(request, *args, **kwargs):
    #queryset = PageVisit.objects.all() # Get all objects
    #page_qs = PageVisit.objects.filter(path=request.path) # Filter for objects with path
    
    my_title = "Home"
    html_template = "home.html" # Set template
    my_context = {
        "page_title": my_title,
        #"page_visit_count": page_qs.count(), # Count all page visit rows that are in query set
        #"total_visit_count": queryset.count(),
        #"percent": (page_qs.count() * 100.0) / queryset.count(),
    }
    path = request.path
    #PageVisit.objects.create(path = request.path) # Create a page visit
    return render(request, html_template, my_context)  # Return response to server

def login_page_view(request, *args, **kwargs):
    my_title = "Login Page"
    my_context = {
        "page_title": my_title
    }
    html_template = "login.html"

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # checks the username and password against auth_user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # starts the session, which is saved in django_session
            login(request, user)
            return redirect("/hello-world/")
        my_context["error"] = "Wrong username or password."

    return render(request, html_template, my_context)

def signup_page_view(request, *args, **kwargs):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            return render(request, "login.html", {"page_title": "Login Page", "error": "That username is taken"})

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect("/hello-world/")
    return redirect("/")

def about_page_view(request, *args, **kwargs):
    my_title = "My Page"
    my_context = {
        "page_title": my_title
    }
    html_template = "about.html"
    return render(request, html_template, my_context)  # Return response to server

def my_old_home_page_view(request, *args, **kwargs):
    my_title = "My Page"
    my_context = {
        "page_title": my_title
    }
    html = """
        <!DOCTYPE html>
        <html>
            <body>
                <h1>{page_title} anything?</h1>
            </body>
        </html>
    """.format(**my_context) # page_title = my_title

    # html_file_path = this_dir / "home.html"   # Append the file name to the found directory
    # html_ = html_file_path.read_text() # Read the html

    return HttpResponse(html)  # Return response to server