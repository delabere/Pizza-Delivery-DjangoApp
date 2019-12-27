# TODO: order imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from orders.models import Price, PizzaTopping, SubTopping, FoodSize, PizzaType, PizzaOrder, SubOrder, SubType, PastaOrder, PastaType, PlatterOrder, PlatterType, SaladOrder, SaladType


def order_status(request):
    if 'admin_form' in request.POST:
        model = f"{request.POST['food_type'][:-1]}Order"
        model = globals()[model]

        order = model.objects.filter(pk=request.POST['id'])
        order.delete()


    models = [PizzaOrder,
              SubOrder,
              PastaOrder,
              SaladOrder,
              PlatterOrder
              ]

    for model in models:
        for item in model.objects.filter(user=request.user.username, status='Draft').all():
            item.status = 'Ordered'
            item.save()

    return HttpResponseRedirect(reverse("index"))

# TODO: add docstrings to all methods


def index(request):
    if request.method == 'POST':
        # create order object for item
        order_data = request.POST

        if 'Pizzas' in order_data['food_type']:
            size = FoodSize.objects.filter(size=order_data['size']).first()
            pizza_type = PizzaType.objects.filter(
                name=order_data['food_item'].split()[0]).first()
            pizza = PizzaOrder(foodsize=size, pizza_type=pizza_type,
                               user=request.user.username, status='Draft')
            pizza.save()
            if 'topping' in order_data:
                toppings = PizzaTopping.objects.filter(
                    name__in=order_data.getlist('topping'))
                pizza.toppings.set(toppings)
            else:
                pizza.reg_pizza_type = 'Special'
                pizza.save()

        elif 'Subs' in order_data['food_type']:
            size = FoodSize.objects.filter(size=order_data['size']).first()
            sub_type = SubType.objects.filter(
                name=order_data['food_item']).first()
            sub = SubOrder(foodsize=size, sub_type=sub_type,
                           user=request.user.username, status='Draft')
            sub.save()
            if 'topping' in order_data:
                toppings = SubTopping.objects.filter(
                    name__in=order_data.getlist('topping'))
                sub.toppings.set(toppings)
            else:
                # sub.reg_pizza_type = 'Special'
                sub.save()

        elif 'Pastas' in order_data['food_type']:
            pasta_type = PastaType.objects.filter(
                name=order_data['food_item']).first()
            pasta = PastaOrder(pasta_type=pasta_type,
                               user=request.user.username, status='Draft')
            pasta.save()

        elif 'Salads' in order_data['food_type']:
            salad_type = SaladType.objects.filter(
                name=order_data['food_item']).first()
            salad = SaladOrder(salad_type=salad_type,
                               user=request.user.username, status='Draft')
            salad.save()

        elif 'Platter' in order_data['food_type']:
            size = FoodSize.objects.filter(size=order_data['size']).first()
            platter_type = PlatterType.objects.filter(
                name=order_data['food_item']).first()
            platter = PlatterOrder(
                foodsize=size, platter_type=platter_type, user=request.user.username, status='Draft')
            platter.save()

    if not request.user.is_authenticated:
        return render(request, "orders/fancy_login.html", {"message": None})

# TODO: remove list()'s here
    basket_data = {
        'Pizzas': [(i.get_price, i) for i in PizzaOrder.objects.filter(user=request.user.username, status='Draft')],
        'Subs': [(i.get_price, i) for i in SubOrder.objects.filter(user=request.user.username, status='Draft')],
        'Pastas': [(i.get_price, i) for i in PastaOrder.objects.filter(user=request.user.username, status='Draft')],
        'Salads': [(i.get_price, i) for i in SaladOrder.objects.filter(user=request.user.username, status='Draft')],
        'Platters': [(i.get_price, i) for i in PlatterOrder.objects.filter(user=request.user.username, status='Draft')],
    }

    basket_amounts = [i for i in basket_data.values()][0]
    basket_total = sum([i[0] for i in basket_amounts])

    checkout_data = {
        'Pizzas': [(i.id, i.user, i) for i in PizzaOrder.objects.filter(status='Ordered')],
        'Subs': [(i.id, i.user, i) for i in SubOrder.objects.filter(status='Ordered')],
        'Pastas': [(i.id, i.user, i) for i in PastaOrder.objects.filter(status='Ordered')],
        'Salads': [(i.id, i.user, i) for i in SaladOrder.objects.filter(status='Ordered')],
        'Platters': [(i.id, i.user, i) for i in PlatterOrder.objects.filter(status='Ordered')]
    }

    context = {
        "user": request.user,
        "basket": basket_data,
        "basket_total": basket_total,
        "checkout": checkout_data,
        "menu": {
            'Pizzas': [str(i) for i in Price.objects.all() if i.food_type == 'Pizza'],
            'Pastas': [str(i) for i in Price.objects.all() if i.food_type == 'Pasta'],
            'Salads': [str(i) for i in Price.objects.all() if i.food_type == 'Salad'],
            'Platters': [str(i) for i in Price.objects.all() if i.food_type == 'Platter'],
            'Subs': [str(i) for i in Price.objects.all() if i.food_type == 'Sub'],
        },
        "pizza_toppings": PizzaTopping.objects.all(),
        "sub_toppings": SubTopping.objects.all(),
    }
    if User.objects.get(username=request.user).is_staff:
        return render(request, "orders/admin.html", context)
    return render(request, "orders/user.html", context)


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/fancy_login.html", {"message": "Invalid credentials."})


def logout_view(request):
    logout(request)
    return render(request, "orders/fancy_login.html", {"message": "Logged out."})


def register_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]

        # if any of the fields are blank - restart registration with message
        for val in [username, password, first_name, last_name, email]:
            if val == '':
                return render(request, "orders/fancy_register.html", {"message": "fill in all fields"})
        try:
            user = User.objects.create_user(
                username=username, email=email, password=password, first_name=first_name, last_name=last_name)
        except IntegrityError:
            return render(request, "orders/fancy_register.html", {"message":  "This username is taken"})
        user.save()
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/fancy_register.html", {"message": "Invalid credentials."})
    return render(request, "orders/fancy_register.html", {"message": None})
