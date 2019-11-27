from django.db import models
from django.core.exceptions import ValidationError
# TODO: add pricing information to all options somehow
# abstract away the sizes and toppings and have pizza/subs inherit those like
# pizza does currently with foodsize

# Create your models here
# Hierarchy:
#   Food_Size
#   PizzaType // SubType
#   PizzaToppings // SubToppings
#   Pizza  // Pasta  //  Sub  //  Platter


class FoodSize(models.Model):
    size = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.size}'


class PizzaType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class SubType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class PlatterType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class PastaType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class SaladType(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class PizzaTopping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class SubTopping(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.name}'


class PizzaOrder(models.Model):
    foodsize = models.ForeignKey(
        FoodSize, on_delete=models.CASCADE, related_name='pizza')
    toppings = models.ManyToManyField(
        PizzaTopping, blank=True, related_name='pizza')
    pizza_type = models.ForeignKey(
        PizzaType,  on_delete=models.CASCADE, related_name='pizza')
    user = models.CharField(max_length=65)

    @property
    def get_price(self):
        topping_count = self.toppings.count()
        if topping_count > 3:
            raise ValidationError("You can't assign more than three regions")

        if self.foodsize.size == 'Small':
            price = Price.objects.get(
                menu_item=f'{self.pizza_type} Pizza {topping_count} Topping', food_type='Pizza').small
        elif self.foodsize.size == 'Large':
            price = Price.objects.get(
                menu_item=f'{self.pizza_type} Pizza {topping_count} Topping', food_type='Pizza').large
        else:
            price = 'none'
        return price

    def __str__(self):
        toppings = ", ".join(str(seg) for seg in self.toppings.all())
        return f'{self.foodsize} {self.pizza_type} with {toppings} Price: {self.get_price}'


class SubOrder(models.Model):
    foodsize = models.ForeignKey(
        FoodSize, on_delete=models.CASCADE, related_name='sub')
    toppings = models.ManyToManyField(
        SubTopping, blank=True, related_name='sub')
    sub_type = models.ForeignKey(
        SubType, on_delete=models.CASCADE, related_name='sub')
    user = models.CharField(max_length=65)

    @property
    def get_price(self):
        # query toppings
        toppings = [top.name for top in self.toppings.all()]
        topping_price = sum([Price.objects.get(menu_item=topping, food_type='Topping').small for topping in toppings])

        if self.foodsize.size == 'Small':
            base_price = Price.objects.get(
                menu_item=self.sub_type, food_type='Sub').small
        elif self.foodsize.size == 'Large':
            base_price = Price.objects.get(
                menu_item=self.sub_type, food_type='Sub').large
        else:
            price = 'none'
        print(base_price)
        if toppings:
            return base_price + topping_price
        else:
            return base_price

    def __str__(self):
        toppings = ", ".join(str(seg) for seg in self.toppings.all())
        return f'{self.foodsize} {self.sub_type} Sub with {toppings} Price: {self.get_price}'


class PlatterOrder(models.Model):
    platter_type = models.ForeignKey(
        PlatterType, on_delete=models.CASCADE, related_name='sub')
    foodsize = models.ForeignKey(
        FoodSize, on_delete=models.CASCADE, related_name='platter')
    user = models.CharField(max_length=65)

    @property
    def get_price(self):
        print(self.foodsize.size)
        if self.foodsize.size == 'Small':
            price = Price.objects.get(
                menu_item=self.platter_type, food_type='Platter').small
        elif self.foodsize.size == 'Large':
            price = Price.objects.get(
                menu_item=self.platter_type, food_type='Platter').large
        else:
            price = 'none'
        return price

    def __str__(self):
        return f'{self.foodsize} {self.platter_type} Price: {self.get_price}'


class PastaOrder(models.Model):
    pasta_type = models.ForeignKey(
        PastaType, on_delete=models.CASCADE, related_name='pasta')
    user = models.CharField(max_length=65)

    @property
    def get_price(self):
        price = Price.objects.get(
            menu_item=self.pasta_type, food_type='Pasta').small
        return price

    def __str__(self):
        return f'{self.pasta_type}'


class Price(models.Model):
    menu_item = models.CharField(max_length=65)
    food_type = models.CharField(max_length=65, choices=[
        ('Pizza', 'Pizza'),
        ('Pasta', 'Pasta'),
        ('Salad', 'Salad'),
        ('Platter', 'Platter'),
        ('Sub', 'Sub'),
        ('Topping', 'Topping')
    ])
    small = models.DecimalField(max_digits=10, decimal_places=2)
    large = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.menu_item}'


class SaladOrder(models.Model):
    salad_type = models.ForeignKey(
        SaladType, on_delete=models.CASCADE, related_name='salad')
    user = models.CharField(max_length=65)

    @property
    def get_price(self):
        price = Price.objects.get(
            menu_item=self.salad_type, food_type='Salad').small
        return price

    def __str__(self):
        return f'{self.salad_type} Price:{self.get_price}'
