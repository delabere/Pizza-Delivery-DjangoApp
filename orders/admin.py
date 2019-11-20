from django.contrib import admin

from orders.models import Pizza, PizzaTopping, Sub, SubTopping, Pasta, Platter, FoodSize
# Register your models here.

admin.site.register(FoodSize)
admin.site.register(Pizza)
admin.site.register(PizzaTopping)
admin.site.register(Sub)
admin.site.register(SubTopping)
admin.site.register(Pasta)
admin.site.register(Platter)