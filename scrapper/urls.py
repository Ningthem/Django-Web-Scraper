from django.urls import path, include
from .api import CheckApi, ScrapWeb, ListProductAPI

app_name="scrapper"

urlpatterns = [
   path('scrapper/check-api/', CheckApi.as_view()),
   path('scrapper/scrap-web/', ScrapWeb.as_view()),
   path('scrapper/product-list/', ListProductAPI.as_view()),
]
