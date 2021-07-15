from office.models import Employee
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
def loginView(request):
  if not request.POST:
    return render(request, 'registration/login.html')
  username = request.POST['username']
  password = request.POST['password']
  user = authenticate(request, username=username, password=password)
  if user is not None:
    login(request, user)
    return redirect('/')
  else:
    return render(request, 'registration/login.html', {
      'errorMessage': 'Incorrect username/password. Please try again!',
    })

@login_required
@never_cache
def logoutView(request):
  logout(request)
  return render(request, 'registration/logged_out.html')
