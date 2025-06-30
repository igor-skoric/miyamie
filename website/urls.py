from django.urls import path
from . import views

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

]
