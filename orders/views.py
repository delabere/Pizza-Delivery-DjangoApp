from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from orders.models import Price, PizzaTopping, SubTopping, FoodSize, PizzaType, PizzaOrder
from django.db.models import Q

# Create your views here.

def index(request):
    if request.method == 'POST':
        # create order object for item
        request.session['orders_item'] = request.POST
        print(request.session['orders_item'])
        if 'Pizzas' in request.session['orders_item']['food_type']:
            order_item = {'food_type': request.session['orders_item']['food_type'],
                        'item_type': request.session['orders_item']['food_item'].split()[0],
                        'size': request.session['orders_item']['size'],
                        'toppings': request.session['orders_item'].getlist('topping'),
                        'joined_toppings': ', '.join(request.session['orders_item'].getlist('topping')),
            }
        elif 'Subs' in request.session['orders_item']['food_type']:
            order_item = {'food_type': request.session['orders_item']['food_type'],
                        'item_type': request.session['orders_item']['food_item'],
                        'size': request.session['orders_item']['size'],
                        'toppings': request.session['orders_item'].getlist('topping'),
                        'joined_toppings': ', '.join(request.session['orders_item'].getlist('topping')),
            }
        else:
            order_item = {'food_type': request.session['orders_item']['food_type'],
                        'item_type': request.session['orders_item']['food_item'],
                        'size': request.session['orders_item']['size'],
            }
        print(order_item)
        request.session['orders_all'].append(order_item)
        print(request.session['orders_all'])



        # size = FoodSize.objects.filter(size=order_item['size']).first()
        # pt = PizzaType.objects.filter(name=order_item['item_type']).first()
        # toppings = PizzaTopping.objects.filter(name__in=order_item['toppings'])
        # p = PizzaOrder(foodsize=size, pizza_type=pt)
        # p = p.save(commit=False)
        # p.toppings.set(toppings)
        # print(p)
        # if request.session['orders_item']['food_type'] == 'pizzas':
        #     size = FoodSize.objects.filter(size=order['size']).first()
            
        #     if 'Regular' in request.session['order']['food_item']:
        #         pizza_type  = PizzaType(name='Regular')
        #     if 'Sicilian' in request.session['order']['food_item']:
        #         pizza_type  = PizzaType(name='Sicilian')

        # print(request.session['order'])

    if not request.user.is_authenticated:
        return render(request, "orders/fancy_login.html", {"message": None})
    # if not hasattr(request.session, 'orders_item'):
    #     request.session['orders_item'] = ''
    # if not hasattr(request.session, 'orders_all'):
    #     request.session['orders_all'] = []

    context = {
        "user": request.user,
        "session": request.session,
        "menu" : {
            'Pizzas' : [str(i) for i in Price.objects.all() if i.food_type == 'Pizza'],
            'Pastas' : [str(i) for i in Price.objects.all() if i.food_type == 'Pasta'],
            'Salads' : [str(i) for i in Price.objects.all() if i.food_type == 'Salad'],
            'Platters' : [str(i) for i in Price.objects.all() if i.food_type == 'Platter'],
            'Subs' : [str(i) for i in Price.objects.all() if i.food_type == 'Sub'],
            },
        "pizza_toppings" : PizzaTopping.objects.all(),
        "sub_toppings" : SubTopping.objects.all(),
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
