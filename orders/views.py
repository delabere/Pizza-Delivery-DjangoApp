from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from orders.models import Price, PizzaTopping, SubTopping, FoodSize, PizzaType, PizzaOrder, SubOrder, SubType, PastaOrder, PastaType, PlatterOrder, PlatterType, SaladOrder, SaladType
from django.db.models import Q
# from django.contrib.sessions.models import Session

from functools import wraps

session_data = {}

# Create your views here.

# In [6]: order_data = {'food_type': 'Pizzas',
#    ...:                 'food_item': 'Regular Pizza 2 Topping',
#    ...:                 'size': 'Small',
#    ...:                 'topping': ['Sausage', 'Ham']}

# def make_order

# TODO: add docstrings to all methods


def index(request):
    if request.method == 'POST':
        # create order object for item
        order_data = request.POST

        # remove 'topping...' from toppings


        # print(request.session['orders_item'])
        # if 'Pizzas' in request.session['orders_item']['food_type']:
        #     order_item = {'food_type': request.session['orders_item']['food_type'],
        #                 'item_type': request.session['orders_item']['food_item'].split()[0],
        #                 'size': request.session['orders_item']['size'],
        #                 'toppings': request.session['orders_item'].getlist('topping'),
        #                 'joined_toppings': ', '.join(request.session['orders_item'].getlist('topping')),
        #     }
        # elif 'Subs' in request.session['orders_item']['food_type']:
        #     order_item = {'food_type': request.session['orders_item']['food_type'],
        #                 'item_type': request.session['orders_item']['food_item'],
        #                 'size': request.session['orders_item']['size'],
        #                 'toppings': request.session['orders_item'].getlist('topping'),
        #                 'joined_toppings': ', '.join(request.session['orders_item'].getlist('topping')),
        #     }
        # else:
        #     order_item = {'food_type': request.session['orders_item']['food_type'],
        #                 'item_type': request.session['orders_item']['food_item'],
        #                 'size': request.session['orders_item']['size'],
        #     }
        # print(order_item)
        # request.session['orders_all'].append(order_item)
        # if 'save' in request.session:
        #     request.session['save'] += 1
        # else:
        #     request.session['save'] = 1
        # print(request.session['orders_all'])

        if 'Pizzas' in order_data['food_type']:
            size = FoodSize.objects.filter(size=order_data['size']).first()
            pizza_type = PizzaType.objects.filter(name=order_data['food_item'].split()[0]).first()
            pizza = PizzaOrder(foodsize=size, pizza_type=pizza_type, user=request.user.username, status='Draft')
            pizza.save()
            if 'topping' in order_data:
                toppings = PizzaTopping.objects.filter(name__in=order_data.getlist('topping'))
                pizza.toppings.set(toppings)
            else:
                pizza.reg_pizza_type = 'Special'
                pizza.save()


        elif 'Subs' in order_data['food_type']:
            size = FoodSize.objects.filter(size=order_data['size']).first()
            sub_type = SubType.objects.filter(name=order_data['food_item']).first()
            sub = SubOrder(foodsize=size, sub_type=sub_type, user=request.user.username, status='Draft')
            sub.save()
            if 'topping' in order_data:
                toppings = SubTopping.objects.filter(name__in=order_data.getlist('topping'))
                sub.toppings.set(toppings)
            else:
                # sub.reg_pizza_type = 'Special'
                sub.save()

        elif 'Pastas' in order_data['food_type']:
            pasta_type = PastaType.objects.filter(name=order_data['food_item']).first()
            pasta = PastaOrder(pasta_type=pasta_type, user=request.user.username, status='Draft')
            pasta.save()

        elif 'Salads' in order_data['food_type']:
            salad_type = SaladType.objects.filter(name=order_data['food_item']).first()
            salad = SaladOrder(salad_type=salad_type, user=request.user.username, status='Draft')
            salad.save()

        elif 'Platter' in order_data['food_type']:
            size = FoodSize.objects.filter(size=order_data['size']).first()
            platter_type = PlatterType.objects.filter(name=order_data['food_item']).first()
            platter = PlatterOrder(foodsize=size, platter_type=platter_type, user=request.user.username, status='Draft')
            platter.save()



    # TODO: should be wrapped in else block - do at end in case of break
    if not request.user.is_authenticated:
        return render(request, "orders/fancy_login.html", {"message": None})
    if not 'orders_item' in request.session:
        request.session['orders_item'] = ''
    if not 'orders_all' in request.session:
        if str(request.user) not in session_data:
            session_data[str(request.user)] = []
        request.session['orders_all'] = session_data[str(request.user)]

    context = {
        "user": request.user,
        "session": request.session,
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
    session_data[str(request.user)] = request.session['orders_all']
    print(session_data)
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

        user = User.objects.create_user(
            username=username, email=email, password=password, first_name=first_name, last_name=last_name)

        user.save()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/fancy_register.html", {"message": "Invalid credentials."})

    return render(request, "orders/fancy_register.html", {"message": None})
