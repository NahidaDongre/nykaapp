from django.contrib import admin

from.models import Product,Brand,UserProfile
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display=["id","pname","price","category","description","is_active","pimage"]
    list_filter=["category","is_active"]
admin.site.register(Product,ProductAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display=["id","bname","price","category","description","is_active","pimage"]
    list_filter=["category","is_active"]
admin.site.register(Brand,BrandAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display=["user","bio","location","birth_date","profile_picture"]
admin.site.register(UserProfile,UserProfileAdmin)