from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from django.contrib import messages
from .decorotars import unauthenticated_user,allowed_user
# Create your views here.
#@login_required(login_url='login')
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


from .Target import get_lo_hi
import pandas as pd
from .problem_giver import give_me_problem
from .weak_tags import get_weak_tags
from Dataset.models import Handle,Pupil,Expert,Candidate_Master,Master,Specialist,Counter
import random
@login_required(login_url='login')
def Recommend(request):
    handle = str(request.user)
    (ase, target) = get_lo_hi(handle)
    if ase == -1:
        messages.error(request,"Something Went Wrong!")
        redirect('recommend')
    print(ase,target)

    if target == 1200:
        Table = Pupil
    if target == 1400:
        Table = Specialist
    if target == 1600:
        Table = Expert
    if target == 1900:
        Table = Candidate_Master
    if target == 2100:
        Table = Master

    Table = pd.DataFrame.from_records(Table.objects.all().values())

    (weak_tags,percentage) = get_weak_tags(handle)
    res = give_me_problem(weak_tags,Table)
    context = {
        'problems':[]
    }
    for i in range(3):
        random_index = random.randint(0,len(res)-1)
        pathabo = Table.iloc[res[random_index]]
        print(pathabo)
        s = pathabo.Tags
        Tags = s.split(',')
        map = {'i':pathabo,'Tags':Tags}
        context['problems'].append(map)
    print(context)
    return render(request,'recommend.html',context)

import requests
@login_required
def Profile(request):
    handle = str(request.user)
    url = 'https://codeforces.com/api/user.info?handles='+handle
    try:
        response = requests.get(url)
        x=response.json()

    except:
        print("Not found") 
    (weak_tags,percentage)=get_weak_tags(handle) 
    info = {
    }
    x=x["result"]
    x=x[0]
    info['handle']=handle
    info['maxRating'] = int(x['maxRating'])
    info['maxRank'] = x['maxRank']
    info['photo'] = x['titlePhoto']
    weak_list=[]
    weak_tags=weak_tags.split(',')
    for i in range(len(percentage)):
        weak_list.append(list([weak_tags[i],percentage[i]]))
    #sorting
    for i in range(len(weak_list)):
        for j in range(i+1,len(weak_list)):
            if weak_list[j][1]>weak_list[i][1]:
                tmp = weak_list[i]
                weak_list[i]=weak_list[j]
                weak_list[j]=tmp

    info['weak_list']=weak_list
    return render(request,'profile.html',info)
