from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def video_list(request):
    return HttpResponse("Welcome to the Videos page!")
