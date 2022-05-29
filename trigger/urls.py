from django.urls import path
from .views import *

urlpatterns = [
    path('trigger', notificationTrigger ),
    path('hospitaltrigger', hospitalNotificationTrigger ),
]