from django.db import models

# Create your models here.
# TODO: create models for: pizzas, toppings, subs, pasta, salads, dinner-platters

class Pizza(models.Model):
    pizza_size = models.CharField(max_length=64)
    pizza_type = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pizza_size} {self.pizza_type}'

class PizzaTopping(models.Model):
    name = models.CharField(max_length=64)
    pizzas = models.ManyToManyField(Pizza, blank=True, related_name='topping')

    def __str__(self):
        return f'{self.name}'


class Sub(models.Model):
    sub_type = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.sub_type}'

class SubTopping(models.Model):
    name = models.CharField(max_length=65)
    subs = models.ManyToManyField(Sub, blank=True, related_name='topping')

    def __str__(self):
        return f'{self.topping}'

class Pasta(models.Model):
    pasta = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pasta}'

class Platter(models.Model):
    platter_type = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.platter_type}'