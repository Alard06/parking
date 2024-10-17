from django.urls import path
from main.views import *

urlpatterns = [
    path('', test),
    path('models/', model_list, name='model_list'),
    path('create-parking/', create_parking, name='create_parking'),
    path('parkings/', parking_list, name='parking_list'),
    path('edit-parking/<int:parking_id>/', edit_parking, name='edit_parking'),
]
