from django.contrib import admin
from .models import Bids, Category, Listing, WatchList, Comments

# Register your models here.
admin.site.register(Bids)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(WatchList)
admin.site.register(Comments)