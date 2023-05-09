from django.contrib import admin
from .models import User
from .models import RideOwner
from .models import RideDriver
from .models import RideSharer

# Register your models here.
admin.site.register(User)
admin.site.register(RideOwner)
admin.site.register(RideDriver)
admin.site.register(RideSharer)
