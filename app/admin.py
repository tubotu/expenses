from django.contrib import admin 
from .models import BigCategory, SmallCategory, Item
 
admin.site.register(BigCategory)
admin.site.register(SmallCategory)
admin.site.register(Item) 