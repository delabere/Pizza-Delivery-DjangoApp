from django.db import models
#TODO: add pricing information to all options somehow
# abstract away the sizes and toppings and have pizza/subs inherit those like
# pizza does currently with foodsize

# Create your models here.
class FoodSize(models.Model):
    size = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.size}'

class Pizza(models.Model):
    pizza_type = models.CharField(max_length=64)
    foodsize = models.ManyToManyField(FoodSize, blank=True, related_name='pizza') 

    def __str__(self):
        return f'{self.foodsize} {self.pizza_type}'



class Sub(models.Model):
    sub_type = models.CharField(max_length=64)
    foodsize = models.ManyToManyField(FoodSize, blank=True, related_name='sub') 

    def __str__(self):
        return f'{self.sub_type}'


class Pasta(models.Model):
    pasta = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pasta}'


class Platter(models.Model):
    platter_type = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.platter_type}'


class PizzaTopping(models.Model):
    name = models.CharField(max_length=64)
    pizzas = models.ManyToManyField(Pizza, blank=True, related_name='topping')

    def __str__(self):
        return f'{self.name}'


class SubTopping(models.Model):
    name = models.CharField(max_length=65)
    subs = models.ManyToManyField(Sub, blank=True, related_name='topping')

    def __str__(self):
        return f'{self.topping}'
