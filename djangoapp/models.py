from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):

    name = models.CharField(null=False, max_length=30, default="Car Maker")
    description = models.TextField(max_length=1000)

    def dealer_id(self):
        car_models = self.carmodel_set.all()
        if car_models.exists():
            return car_models.first().dealer_id
        else:
            return None

    def __str__(self):
        return self.name


class CarModel(models.Model):

    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField(default=0)
    name = models.CharField(max_length=200, default="Model")

    SEDAN = "sedan"
    SUV = "suv"
    WAGON = "wagon"
    COUPE = "coupe"

    TYPE_CHOICES = [
        (SEDAN, "Sedan"),
        (SUV, "Suv"),
        (WAGON, "Wagon"),
        (COUPE, "Coupe")
    ]

    car_type = models.CharField(
        null=False,
        max_length=20,
        choices=TYPE_CHOICES,
        default=SEDAN
    )

    car_year = models.DateField(null=True)

    def __str__(self):
        return self.name

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer state
        self.state = state
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return self.full_name



class DealerReview:

    def __init__(self, dealership, name, purchase, review, id, purchase_date, car_make, car_model, car_year, sentiment):
        # Review Dealership
        self.dealership = dealership
        # User Name
        self.name = name
        # Purchase Status
        self.purchase = purchase
        # User Review
        self.review = review
        # Review Id
        self.id = id
        # Purchase Date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # User Sentiment
        self.sentiment = sentiment

        def __str__(self):
            return self.review