from django.urls import path
from . import views
# from website.utils.google_calendar import connect_google, oauth2callback

urlpatterns = [
    path('', views.home, name='home'),

    path('showroom', views.showroom, name='showroom'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('confirmation', views.confirmation, name='confirmation'),
    path('single_product/<int:pk>', views.single_product, name='single_product'),
    path('products/<slug:slug>', views.products, name='products'),

    path('appointment/', views.appointment_form, name='appointment'),
    path('get-available-times/', views.get_available_times, name='get_available_times'),

    # path('connect-google/', connect_google, name='connect_google'),
    # path('oauth2callback/', oauth2callback, name='oauth2callback'),
    # path('reservation/', views.create_reservation_view, name='reservation'),

]
