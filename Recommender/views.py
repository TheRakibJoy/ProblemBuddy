from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from django.contrib import messages
from .decorotars import unauthenticated_user,allowed_user
# Create your views here.
@login_required(login_url='login')
def Home(request):
   return render(request,'home.html')

@unauthenticated_user
def LogIn(request):
      if request.method=='POST':
         username = request.POST.get('username')
         password = request.POST.get('password')
         user = authenticate(request,username=username,password=password)
         if user is not None:
             login(request,user)
             return redirect('home')

         else:
            messages.info(request,"Username or Password is incorrect.")
      return render(request, 'login.html')


@login_required(login_url='login')
def LogOut(request):
   logout(request)
   return redirect('login')

@unauthenticated_user
def Register(request):
      form = CreateUserForm()
      if request.method=='POST':
         form=CreateUserForm(request.POST)
         if form.is_valid():
            user = form.save()
            handle = form.cleaned_data.get('username')
            group = Group.objects.get(name='contestant')
            user.groups.add(group)
            messages.success(request,'Account was created for user '+handle)

            return redirect('login')

      context = {'form': form}
      return render(request, 'register.html', context)


@login_required(login_url='login')
def Recommend(request):
   return HttpResponse(request.user)