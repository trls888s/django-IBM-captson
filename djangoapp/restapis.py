import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a get_dealers_from_cf method to get dealers from a cloud function

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    response = requests.get(url, params=kwargs)
    data = response.json()
    dealerships = data.get('docs', [])
    # For each dealership object
    for dealership in dealerships:
        # Create a CarDealer object with values from the dealership dictionary
        dealer_obj = CarDealer(
            address=dealership["address"],
            city=dealership["city"],
            full_name=dealership["full_name"],
            id=dealership["id"],
            lat=dealership["lat"],
            long=dealership["long"],
            short_name=dealership["short_name"],
            st=dealership["st"],
            state=dealership["state"],
            zip=dealership["zip"]
        )
        results.append(dealer_obj)
    return results



# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function

def get_dealer_reviews_from_cf(url, dealerId):
    reviews_list = []
    response = requests.get(url, params={'dealerId':dealerId})
    data = response.json()
    results = data.get('docs', [])

    for review in results:
            review_object = DealerReview(
                dealership=review.get("dealership", ""),
                name=review.get("name", ""),
                purchase=review.get("purchase", ""),
                id=review.get("id", ""),
                review=review.get("review", ""),
                purchase_date=review.get("purchase_date", ""),
                car_make=review.get("car_make", ""),
                car_model=review.get("car_model", ""),
                car_year=review.get("car_year", ""),
                sentiment="",
            )
            review_object.sentiment = analyze_review_sentiments(review_object.review)
            reviews_list.append(review_object)
    return reviews_list

# Create a `post_request` to make HTTP POST requests

def post_request(url, json_payload, **kwargs):

    try:
        response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'}, 
                                 json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    
    return json_data




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text

def analyze_review_sentiments(text): 

        url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/3b742a58-aa4f-4bc1-8a71-d36c44eb2084" 

        api_key = "iAD7uu5BtUVk9xWs5HeVz2dn4pLqI4MmK4_LTBvWAJzP" 

        authenticator = IAMAuthenticator(api_key) 

        natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

        natural_language_understanding.set_service_url(url) 

        response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text])), language="en").get_result() 

        label=json.dumps(response, indent=2) 

        label = response['sentiment']['document']['label'] 

        return(label) 

