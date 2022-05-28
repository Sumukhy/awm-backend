from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import messaging
import geopy.distance
import json


latitude = 10
longitude = 10

cred = credentials.Certificate("C:/Users/SUMUKH_YR/Desktop/amw-firebase-firebase-adminsdk-x47ac-a650a4438a.json")
firebase_admin.initialize_app(cred)
    


def calc_dist(lat1, lon1):
    loc1 = (latitude, longitude)
    loc2 = (lat1, lon1)
    return geopy.distance.distance(loc1, loc2).km

def sendNotification(uid):
    message = messaging.Message(notification=messaging.Notification(title = 'Acc within 1Km please help me',
                                                                    body = "Please help me" ), 
                                topic=uid,
                                data = {'lat': str(latitude), 'long' : str(longitude)})
    response = messaging.send(message)
    

    
def trigger():
    
    db = firestore.client()
    user_list = db.collection('users').get()
    
    for user in user_list:
        print(user.id)
        user_lat = user.get('lat')
        user_lon = user.get('lon')
        distance = calc_dist(user_lat, user_lon)
        if distance < 2 :
            print(f"sending notification to {user.id} distance - {distance}")
            sendNotification(user.id)

# Create your views here.
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def notificationTrigger(request):
    global latitude, longitude
    lat = request.GET.get('lat')
    lon = request.GET.get('long')
    latitude = float(lat)
    longitude = float(lon)
    trigger()
    return Response({"status": "success"})