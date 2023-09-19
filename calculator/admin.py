from django.contrib import admin
from .models import UserProfileModel, MarketCreatedModel, ItemCreatedModel

# Register your models here.


@admin.register(UserProfileModel)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "wage",]


@admin.register(MarketCreatedModel)
class MarketCreatedAdmin(admin.ModelAdmin):
    search_fields = ["name__icontains",]
    list_display = ["name", "user_id", "distance", "favorite"]
    list_filter = ["user_id", "favorite"]


@admin.register(ItemCreatedModel)
class ItemCreatedAdmin(admin.ModelAdmin):
    search_fields = ["name__icontains", "price__icontains",]
    list_display = ["name", "price", "market_id", "item_owner"]
    list_editable = ["price"]
    list_per_page = 20

    def item_owner(self, product):
        return product.market_id.user_id.username
