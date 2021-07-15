from django.urls import path

from . import views

app_name = 'office'
urlpatterns = [
  path('', views.home, name='home'),
  path('profile/', views.profile, name='profile'),
  path('profile/mark', views.mark, name='mark'),
  path('profile/history', views.history, name='history'),
  path('profile/change_password', views.changePassword, name='changePassword'),
  path('profile/employee/<str:username>', views.empHistory, name='empHistory'),
  path('addEmployee/', views.addEmployee, name='addEmployee'),
]
