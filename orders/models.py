from django.db import models

# Create your models here.
# TODO: create models for: pizzas, toppings, subs, pasta, salads, dinner-platters

class Pizza(models.Model):
    pizza_type = models.CharField(max_length=64)
    pizza_size = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pizza_size} {self.pizza_type}'

class PizzaToppings(models.Model):
    topping = models.ManyToManyField(Pizza, blank=True, related_name='toppings')

    def __str__(self):
        return f'{self.topping}'


class Subs(models.Model):
    sub_type = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.sub_type}'

class SubToppings(models.Model):
    topping = models.ManyToManyField(Subs, blank=True, related_name='toppings')

    def __str__(self):
        return f'{self.topping}'

class Pasta(models.Model):
    pasta = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pasta}'

class Platters(models.Model):
    platter_type = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.platter_type}'