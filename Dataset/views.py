from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def Train(request):
    return render(request, 'input_handle.html')