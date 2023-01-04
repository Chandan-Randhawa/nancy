from django.contrib import admin
from django.urls import path 
from wht_eml import views

urlpatterns = [
    path('', views.index , name = 'index'),
    path('whtsapp', views.whtsapp , name = 'whtsapp'),
    path('emaill', views.emaill , name = 'emaill'),
]
