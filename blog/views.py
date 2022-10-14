from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
  return HttpResponse("Hello, world.")
def login_page(request):
  return HttpResponse("Login")