from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from orders.models import Price, PizzaTopping, SubTopping, FoodSize

# Create your views here.

def index(request):
    if request.method == 'POST':
        # create order object for item
        request.session['order'] = request.POST
        if request.session['order']['food_type'] == 'pizzas':
            size = FoodSize(size=request.session['order']['size'])
            #  = FoodSize(size=request.session['order']['size'])


        print(request.session['order'])

    if not request.user.is_authenticated:
        return render(request, "orders/fancy_login.html", {"message": None})
    if not hasattr(request.session, 'order'):
        request.session.order = ''
    context = {
        "user": request.user,
        "session": request.session,
        "menu" : {
            'pizzas' : [str(i) for i in Price.objects.all() if i.food_type == 'Pizza'],
            'pastas' : [str(i) for i in Price.objects.all() if i.food_type == 'Pasta'],
            'salads' : [str(i) for i in Price.objects.all() if i.food_type == 'Salad'],
            'platters' : [str(i) for i in Price.objects.all() if i.food_type == 'Platter'],
            'subs' : [str(i) for i in Price.objects.all() if i.food_type == 'Sub'],
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
