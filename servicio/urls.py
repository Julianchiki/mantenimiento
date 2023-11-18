from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.signin, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.signout, name='logout'),
    path('car', views.car, name='car'), 
    path('add_car', views.add_car, name='add_car'), 
    path('edit_car', views.edit_car, name='edit_car'), 
    path('delete_car', views.delete_car, name='delete_car'), 
    path('request', views.request, name='request'), 
    path('quote', views.quote, name='quote'), 
    path('add_quote', views.add_quote, name='add_quote'), 
    path('cancel_quote', views.cancel_quote, name='cancel_quote'), 
    path('procces', views.procces, name='procces'), 
    path('complete', views.complete, name='complete'), 
    path('record', views.record, name='record'), 
]