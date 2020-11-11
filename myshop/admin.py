from django.contrib import admin

from .models import UserProfile, Item, Order, Refund


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Refund)
