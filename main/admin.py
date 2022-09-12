from django.contrib import admin
from main.models import User, Product, Category, Order

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)