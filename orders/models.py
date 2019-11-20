from django.db import models
#TODO: add pricing information to all options somehow
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

class PizzaTopping(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'


class SubTopping(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return f'{self.name}'


class Pizza(models.Model):
    foodsize = models.ManyToManyField(FoodSize, blank=True, related_name='pizza') 
    toppings = models.ManyToManyField(PizzaTopping, blank=True, related_name='pizza') 
    pizza_type = models.ManyToManyField(PizzaType, blank=True, related_name='pizza')


    def __str__(self):
        return f'{self.foodsize} {self.pizza_type}'



class Sub(models.Model):
    foodsize = models.ManyToManyField(FoodSize, blank=True, related_name='sub') 
    toppings = models.ManyToManyField(PizzaTopping, blank=True, related_name='sub') 
    sub_type = models.ManyToManyField(SubType, blank=True, related_name='sub')

    def __str__(self):
        return f'{self.foodsize} {self.sub_type}'


class Pasta(models.Model):
    pasta = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.pasta}'


class Platter(models.Model):
    platter_type = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.platter_type}'

