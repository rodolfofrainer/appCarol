from django.contrib import admin
from .models import UserProfileModel, MarketCreatedModel, ItemCreatedModel

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "wage"]

class MarketCreatedAdmin(admin.ModelAdmin):
    list_display = ["name", "user_id", "distance", "favorite"]
    list_filter = ["user_id", "favorite"]
    

class ItemCreatedAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "market_id"]

admin.site.register(UserProfileModel, UserProfileAdmin)
admin.site.register(MarketCreatedModel, MarketCreatedAdmin)
admin.site.register(ItemCreatedModel, ItemCreatedAdmin)