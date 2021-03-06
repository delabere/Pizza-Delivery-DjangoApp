from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from orders.models import Price, PizzaTopping, SubTopping, FoodSize, PizzaType, PizzaOrder, SubOrder, SubType, PastaOrder, PastaType, PlatterOrder, PlatterType, SaladOrder, SaladType


def index(request):
    """
    If a user is authenticated then this controls menu and ordering.
    If an admin is authenticated then this controls the showing of orders and marking orders
    complete
    """

    if not request.user.is_authenticated:
        return render(request, "orders/fancy_login.html", {"message": None})

    if request.method == 'POST':
        # create order object for item
        order_data = request.POST
        order_to_basket(order_data, request)

    basket_data, basket_total = get_basket_contents(request)
    checkout_data = get_processed_orders()

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

    # redirect depending on admin or user profile
    if User.objects.get(username=request.user).is_staff:
        return render(request, "orders/admin.html", context)
    else:
        return render(request, "orders/user.html", context)

def login_view(request):
    """allows a user to login"""
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "orders/fancy_login.html", {"message": "Invalid credentials."})


def logout_view(request):
    """allows a user to logout"""
    logout(request)
    return render(request, "orders/fancy_login.html", {"message": "Logged out."})


def register_view(request):
    """allows a new user to register their information"""
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


def order_status(request):
    """
    if user: marks all basket items as 'Ordered'
    if admin: marks selected order as 'Complete'
    """

    if 'admin_form' in request.POST:
        model = f"{request.POST['food_type'][:-1]}Order"
        model = globals()[model]

        order = model.objects.filter(pk=request.POST['id']).first()
        order.status = 'Complete'
        order.save()

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


def order_to_basket(order_data, request):
    """creates a 'draft' order entry in the database"""
    models = {
        'Pastas': (PastaType, PastaOrder),
        'Salads': (SaladType, SaladOrder),
        'Platters': (PlatterType, PlatterOrder),
        'Pizzas': (PizzaType, PizzaOrder, PizzaTopping),
        'Subs': (SubType, SubOrder, SubTopping),
    }

    # get all the required query data from order
    food_type = models[order_data['food_type']][0].objects.filter(
        name=order_data['food_item']).first()

    if order_data['food_type'] in ['Pizzas', 'Subs', 'Platters']:
        if order_data['food_type'] == 'Pizzas':
            food_type = PizzaType.objects.filter(
                name=order_data['food_item'].split()[0]).first()
        size = FoodSize.objects.filter(size=order_data['size']).first()
        food = models[order_data['food_type']][1](food_type=food_type,
         user=request.user.username, status='Draft', foodsize=size)
    else:
        food = models[order_data['food_type']][1](food_type=food_type,
         user=request.user.username, status='Draft')
    food.save()

    # if pizza or sub then add any toppings
    if 'topping' in order_data:
        toppings = models[order_data['food_type']][2].objects.filter(name__in=order_data.getlist('topping'))
        food.toppings.set(toppings)
        food.save()
    else:
        if order_data['food_type'] == 'Pizzas':
            food.reg_pizza_type = 'Special'
        food.save()


def get_processed_orders():
    """retrieve all 'ordered' orders"""
    checkout_data = {
        'Pizzas': [(i.id, i.user, i) for i in PizzaOrder.objects.filter(status='Ordered')],
        'Subs': [(i.id, i.user, i) for i in SubOrder.objects.filter(status='Ordered')],
        'Pastas': [(i.id, i.user, i) for i in PastaOrder.objects.filter(status='Ordered')],
        'Salads': [(i.id, i.user, i) for i in SaladOrder.objects.filter(status='Ordered')],
        'Platters': [(i.id, i.user, i) for i in PlatterOrder.objects.filter(status='Ordered')]
    }
    return checkout_data


def get_basket_contents(request):
    """get basket orders for current user"""
    basket_data = {
        'Pizzas': [(i.get_price, i) for i in PizzaOrder.objects.filter(user=request.user.username, status='Draft')],
        'Subs': [(i.get_price, i) for i in SubOrder.objects.filter(user=request.user.username, status='Draft')],
        'Pastas': [(i.get_price, i) for i in PastaOrder.objects.filter(user=request.user.username, status='Draft')],
        'Salads': [(i.get_price, i) for i in SaladOrder.objects.filter(user=request.user.username, status='Draft')],
        'Platters': [(i.get_price, i) for i in PlatterOrder.objects.filter(user=request.user.username, status='Draft')],
    }

    basket_amounts = [i for i in basket_data.values()][0]
    basket_total = sum([i[0] for i in basket_amounts])
    return basket_data, basket_total
