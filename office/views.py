from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import never_cache
from django.contrib.auth.hashers import check_password

from .models import Entry, Employee

def today():
  return timezone.localtime(timezone.now()).date()

@never_cache
def home(request):
  if request.user.is_authenticated:
    return redirect('office:profile')
  else:
    return render(request, 'office/home.html')

@login_required
@user_passes_test(lambda user: user.isAdmin)
@never_cache
def empHistory(request, username):
  targetEmployee = get_object_or_404(Employee, username=username)
  return render(request, 'office/history.html', {
    'name': username,
    'record': targetEmployee.history(7),
  })

@login_required
@never_cache
def profile(request):
  if request.user.isAdmin:
    return render(request, 'office/employeeAdmin.html', {
      'employeeAdminName': request.user.username,
      'employees': Employee.objects.filter(
        isAdmin = False,
        is_superuser = False,
      ),
    })
  else:
    return render(request, 'office/employee.html', {
      'employee': request.user,
    })


@login_required
@user_passes_test(lambda user: not user.isAdmin)
@never_cache
def mark(request):
  try:
    Entry.objects.get(employee=request.user, date=today())
  except Entry.DoesNotExist:
    Entry.objects.create(employee=request.user, date=today())
  return redirect('office:profile')


@login_required
@user_passes_test(lambda user: not user.isAdmin)
@never_cache
def history(request):
  return render(request, 'office/history.html', {
    'record' : request.user.history(7),
  })

@never_cache
@login_required
@user_passes_test(lambda user: user.isAdmin)
def addEmployee(request):
  if not request.POST:
    return render(request, 'office/addEmployee.html')
  firstName = request.POST['first_name']
  lastName  = request.POST['last_name']
  email     = request.POST['email']
  username  = request.POST['username']
  password  = request.POST['password']

  emailExists = Employee.objects.filter(email=email).exists()
  if emailExists:
    return render(request, 'office/addEmployee.html', {
      'errorMessage': 'Email already in use!',
    })
  usernameExists = Employee.objects.filter(username=username).exists()
  if usernameExists:
    return render(request, 'office/addEmployee.html', {
      'errorMessage': 'This username has already been chosen. Please user another one!',
    })

  Employee.objects.create_user(
    first_name=firstName,
    last_name=lastName,
    email=email,
    password=password,
    username=username,
    isAdmin=False,
  )

  return render(request, 'office/addEmployee.html', {
    'successMessage': f'User {username} has been created successfully!',
  })

def checkPassword(currentPassword, newPassword, confirmPassword, hashPassword):
  if not check_password(currentPassword, hashPassword):
    return False, 'Incorrect current password'
  if confirmPassword != newPassword:
    return False, 'New passwords do not match'
  if currentPassword == newPassword:
    return False, 'New password cannot be old password'
  if newPassword == '':
    return False, 'New password cannot be empty'

  return True, 'Password changed successfully'

@never_cache
@login_required
def changePassword(request):
  if not request.POST:
    return render(request, 'office/changePassword.html')
  currentPassword = request.POST['currentPassword']
  newPassword = request.POST['newPassword']
  confirmPassword = request.POST['confirmPassword']

  isValid, message = checkPassword(
    currentPassword,
    newPassword,
    confirmPassword,
    request.user.password,
  )

  if isValid:
    request.user.set_password(newPassword)
    request.user.save()

  return render(request, 'office/changePassword.html', {
    'message': message,
    'success': isValid,
  })
