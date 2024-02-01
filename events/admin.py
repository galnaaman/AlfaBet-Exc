from django.contrib import admin
from .models import *

admin.site.site_header = "Events AlfaBet Admin"
admin.site.site_title = "Events AlfaBet Admin "
admin.site.index_title = "Welcome to Events AlfaBet Admin Portal"
admin.site.site_url = "/swagger"

admin.site.register(Event)

