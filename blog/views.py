from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Hello, world.")
def detail(request):
    return HttpResponse("detail page")
def index(request):
    return render(request, "blog/index.html")