from django.contrib import admin
from .models import Human, PasswordStorage, User
# register your models here.

admin.site.register(User)

admin.site.register(Human)

admin.site.register(PasswordStorage)