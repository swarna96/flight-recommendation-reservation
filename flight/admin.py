

# Register your models here.
from django.contrib import admin
from .models import Flight
from .models import Input_Data
from .models import Contact
admin.site.register(Flight)
admin.site.register(Input_Data)
admin.site.register(Contact)