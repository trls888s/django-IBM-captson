from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create an `about` view to render a static about page

def about_view(request):
    endpoint = request.path
    context = {'endpoint': endpoint}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page

def contact_view(request):
    endpoint = request.path
    context = {'endpoint': endpoint}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request

def login_view(request):
    context={}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ccc880f-504c-4f24-a816-b01352454616/dealership-package/get-dealership"
    dealerships = get_dealers_from_cf(url)
    context["dealership_list"]=dealerships
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
    else:
        return render(request, 'djangoapp/index.html', context)

# Create a `logout_request` view to handle sign out request

def logout_view(request):
    context={}
    url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ccc880f-504c-4f24-a816-b01352454616/dealership-package/get-dealership"
    dealerships = get_dealers_from_cf(url)
    # Concat all dealer's short name
    context["dealership_list"]=dealerships
    logout(request)
    return render(request, 'djangoapp/index.html', context)


# Create a `registration_request` view to handle sign up request

def registration_view(request):
    context = {}
    if request.method == "GET":
        return render(request, "djangoapp/registration.html", context)
    elif request.method == "POST":
        # Check if user exists
        username = request.POST["username"]
        password = request.POST["psw"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        user_exist = False
        try:
            User.objects.get(username = username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username = username, first_name = first_name, 
                                            last_name = last_name, password = password)
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            return render(request, 'djangoapp/index.html', context)
      

# Update the `get_dealerships` view to render the index page with a list of dealerships

def get_dealerships(request):

    if request.method == "GET":

        context = {}

        st = request.GET.get("st")
        dealerId = request.GET.get("dealerId")
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ccc880f-504c-4f24-a816-b01352454616/dealership-package/get-dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)

        if st:
            dealerships = get_dealers_from_cf(url, st=st)
        elif dealerId:
            dealerId = int(dealerId)
            dealerships = get_dealers_from_cf(url, dealerId=dealerId)

        context["dealership_list"] = dealerships

        return render(request, "djangoapp/index.html", context=context)


# Create a `get_dealer_details` view to render the reviews of a dealer

def get_dealer_details(request, dealer_id):

    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/7ccc880f-504c-4f24-a816-b01352454616/dealership-package/get-review"
        
        dealer = get_dealer_reviews_from_cf(dealer_url, dealer_id)
       
        context = {
            "reviews": dealer,
            "dealer_id": dealer_id,
        }      
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review

def add_review(request, dealer_id):
    if request.method == "GET":
        cars = CarModel.objects.filter(dealer_id=dealer_id)
        context = { "cars": cars, "dealer_id": dealer_id }
        return render(request, "djangoapp/add_review.html", context)
    
    if request.method == "POST":
        carId = request.POST.get("car")
        car = CarModel.objects.get(id=carId)
        purchase = "false"
        if request.POST.get("purchasecheck") == "on":
            purchase = "true"
        review_data = request.POST
        review = {"review": {}}
        review["review"]["time"] = datetime.utcnow().isoformat()
        review["review"]["dealership"] = dealer_id
        review["review"]["review"] = review_data.get("content", "")
        review["review"]["name"] = request.user.first_name
        review["review"]["purchase"] = purchase
        review["review"]["purchase_date"] = review_data.get("purchasedate", "")
        review["review"]["car_make"] = car.car_make.name
        review["review"]["car_model"] = car.name
        review["review"]["car_year"] = car.car_year.strftime("%Y")

        response = post_request(
            "https://us-south.functions.appdomain.cloud/api/v1/web/7ccc880f-504c-4f24-a816-b01352454616/dealership-package/post-review",
            review,
            dealerId=dealer_id
        )
        
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
       
