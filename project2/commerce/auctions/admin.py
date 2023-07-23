from django.contrib import admin
from .models import List, Comment, Watchlist, Category, Bid

# Register your models here.

admin.site.register(List)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Category)
admin.site.register(Bid)
