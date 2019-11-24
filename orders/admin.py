from django.contrib import admin

from orders.models import FoodSize, PizzaType, SubType, PlatterType, PastaType, SaladType, PizzaTopping, SubTopping, PizzaOrder, SubOrder, PlatterOrder, PastaOrder, SaladOrder

# Register your models here.
admin.site.register(FoodSize)
admin.site.register(PizzaType)
admin.site.register(SubType)
admin.site.register(PlatterType)
admin.site.register(PastaType)
admin.site.register(SaladType)
admin.site.register(PizzaTopping)
admin.site.register(SubTopping)
admin.site.register(PizzaOrder)
admin.site.register(SubOrder)
admin.site.register(PlatterOrder)
admin.site.register(PastaOrder)
admin.site.register(SaladOrder)
