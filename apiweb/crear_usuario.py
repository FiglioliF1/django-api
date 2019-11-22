#from getpass import getpass
#from django.contrib.auth.models import User
#name = input("Ingrese nombre: ")
#email = input("Ingrese email: ")
#passwd = getpass("Ingrese password: ")
#user = User.objects.create_user(username=name, email=email, password=passwd)

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
    	name = input("Ingrese nombre: ")
    	email = input("Ingrese email: ")
    	passwd = getpass("Ingrese password: ")
    	user = User.objects.create_user(username=name, email=email, password=passwd)