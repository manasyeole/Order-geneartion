from django.contrib import admin
from .models import Order
from .models import Item
from .models import MS_list
from .models import Stock


admin.site.register(Order)
admin.site.register(Item)
admin.site.register(MS_list)
admin.site.register(Stock)