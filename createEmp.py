import django
django.setup()
from office.models import Employee
from getpass import getpass

username = input("Username: ")
password = getpass()
first_name = input("First name: ")
last_name = input("Last name: ")
email = input("E-mail ID: ")
isAdmin = input("Admin? [y/N]")
isAdmin = True if isAdmin in ["y", "Y"] else False

employee = Employee.objects.create_user(
    first_name=first_name,
    last_name=last_name,
    email=email,
    password=password,
    username=username,
    isAdmin=isAdmin,
)
print(f"User {employee} created succesfully!")

