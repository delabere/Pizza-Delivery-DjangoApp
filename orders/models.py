from django.db import models
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

    def __str__(self):
        toppings = ", ".join(str(seg) for seg in self.toppings.all())
        return f'{self.foodsize} {self.pizza_type} with {toppings}'


class SubOrder(models.Model):
    foodsize = models.ForeignKey(
        FoodSize, on_delete=models.CASCADE, related_name='sub')
    toppings = models.ManyToManyField(
        SubTopping, blank=True, related_name='sub')
    sub_type = models.ForeignKey(
        SubType, on_delete=models.CASCADE, related_name='sub')

    def __str__(self):
        toppings = ", ".join(str(seg) for seg in self.toppings.all())
        return f'{self.foodsize} {self.sub_type} Sub with {toppings}'


class PlatterOrder(models.Model):
    platter_type = models.ForeignKey(
        PlatterType, on_delete=models.CASCADE, related_name='sub')
    foodsize = models.ForeignKey(
        FoodSize, on_delete=models.CASCADE, related_name='platter')

    def __str__(self):
        return f'{self.foodsize} {self.platter_type}'


class PastaOrder(models.Model):
    pasta_type = models.ForeignKey(
        PastaType, on_delete=models.CASCADE, related_name='pasta')

    def __str__(self):
        return f'{self.pasta_type}'


class SaladOrder(models.Model):
    salad_type = models.ForeignKey(
        SaladType, on_delete=models.CASCADE, related_name='salad')

    def __str__(self):
        return f'{self.salad_type}'
