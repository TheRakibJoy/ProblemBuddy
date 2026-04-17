from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views.decorators.http import require_POST
from .forms import CreateUserForm
from django.contrib import messages
from .decorators import unauthenticated_user
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


@require_POST
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
            group, _ = Group.objects.get_or_create(name='contestant')
            user.groups.add(group)
            messages.success(request,'Account was created for user '+handle)

            return redirect('login')

      context = {'form': form}
      return render(request, 'register.html', context)


import random

from Dataset.codeforces import CodeforcesError, user_info
from Dataset.models import Problem

from .Target import get_lo_hi
from .problem_giver import give_me_problem
from .weak_tags import get_weak_tags


@login_required(login_url='login')
def Recommend(request):
    handle = str(request.user)
    current, target, tier = get_lo_hi(handle)
    if current == -1:
        messages.error(request, "Codeforces is unreachable. Please try again shortly.")
        return render(request, 'recommend.html', {'problems': []})

    weak_tags, _percentage = get_weak_tags(handle)
    ranked = give_me_problem(handle, weak_tags, tier)
    problems = list(Problem.objects.filter(tier=tier).order_by('id'))

    picks = random.sample(ranked, min(3, len(ranked))) if ranked else []
    context = {
        'problems': [
            {'i': problems[i], 'Tags': [t.strip() for t in (problems[i].Tags or '').split(',')]}
            for i in picks
        ]
    }
    return render(request, 'recommend.html', context)


@login_required(login_url='login')
def Profile(request):
    handle = str(request.user)
    try:
        info_payload = user_info(handle)
    except CodeforcesError:
        messages.error(request, "Could not reach Codeforces to load your profile.")
        return render(request, 'profile.html', {'handle': handle, 'weak_list': []})

    weak_tags_str, percentage = get_weak_tags(handle)
    weak_tags = [t.strip() for t in weak_tags_str.split(',') if t.strip()] if weak_tags_str else []
    weak_list = sorted(zip(weak_tags, percentage), key=lambda p: p[1], reverse=True)

    context = {
        'handle': handle,
        'maxRating': int(info_payload.get('maxRating', 0)),
        'maxRank': info_payload.get('maxRank', 'unrated'),
        'photo': info_payload.get('titlePhoto', ''),
        'weak_list': weak_list,
    }
    return render(request, 'profile.html', context)
