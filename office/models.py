import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

def today():
  return timezone.localtime(timezone.now()).date()

def oneDay():
  return datetime.timedelta(days=1)

class Employee(AbstractUser):
  isAdmin = models.BooleanField('Admin', default=False)

  def __str__(self):
    return self.username

  def joinDate(self):
    return self.date_joined.date()

  def isPresent(self, date=today()):
    try:
      Entry.objects.get(
         employee = self,
         date = date,
       )
      return True
    except Entry.DoesNotExist:
      return False

  def history(self, numDays):
    present = {}
    
    curDate = today()
    while curDate >= self.joinDate():
      present[curDate] = False
      curDate -= oneDay()
    
    entries = Entry.objects.filter(
      employee = self,
      date__lte = today(),
      date__gte = self.joinDate(),
    ).order_by('-date')[:numDays]

    for entry in entries:
      present[entry.date] = True

    return present


class Entry(models.Model):
  employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
  date     = models.DateField('Date')

  def __str__(self):
    return str(self.employee) + ', ' + str(self.date)
