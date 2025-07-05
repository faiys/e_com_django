from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(customers)
admin.site.register(store)
admin.site.register(orders)
admin.site.register(orderitems)
admin.site.register(shipsaddress)



