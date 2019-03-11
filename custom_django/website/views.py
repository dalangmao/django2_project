from django.shortcuts import render
from .models import WebsiteArticles

def website_title(request):
    websites = WebsiteArticles.objects.all()
    return render(request, "website/titles.html", {"websites":websites})
