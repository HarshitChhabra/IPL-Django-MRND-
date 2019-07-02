from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Season)
admin.site.register(Matches)
admin.site.register(Innings)
admin.site.register(Overs)
admin.site.register(Deliveries)
#admin.site.register(Delivery_Extra_Data)