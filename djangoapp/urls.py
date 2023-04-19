from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # route is a string contains a URL pattern
    # view refers to the view function
    # name the URL

    # path for about view
    path(route='about/', view=views.about_view, name='about-us'),
    # path for contact us view
    path(route='contact/', view=views.contact_view, name='contact-us'),
    # path for registration
    path(route='registration/', view=views.registration_view, name='registration'),
    # path for login
    path(route='login/', view=views.login_view, name='login'),
    # path for logout
    path(route='logout/', view=views.logout_view, name='logout'),

    path(route='', view=views.get_dealerships, name='index'),

    # path for dealer reviews view
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),

    # path for add a review view
    path(route='dealer/add-review/<int:dealer_id>', view=views.add_review, name="add_review")

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
