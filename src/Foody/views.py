import pathlib
from django.shortcuts import render
from django.http import HttpResponse

from visits.models import PageVisit # Import custom page visit module

this_dir = pathlib.Path(__file__).resolve().parent  # Find (resolve) the parent directory

def home_page_view(request, *args, **kwargs):
    queryset = PageVisit.objects.all() # Get all objects
    page_qs = PageVisit.objects.filter(path=request.path) # Filter for objects with path
    
    my_title = "My Page"
    my_context = {
        "page_title": my_title,
        "page_visit_count": page_qs.count(), # Count all page visit rows that are in query set
        "total_visit_count": queryset.count(),
        "percent": (page_qs.count() * 100.0) / queryset.count(),
    }
    path = request.path
    print("path", path)
    html_template = "home.html" # Set template
    PageVisit.objects.create(path = request.path) # Create a page visit
    return render(request, html_template, my_context)  # Return response to server

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