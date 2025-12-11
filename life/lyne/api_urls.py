# your_app/api_urls.py
from django.urls import path
from . import api_views

urlpatterns = [

 path("verify-face/", api_views.verify_face, name="verify_face"),
]