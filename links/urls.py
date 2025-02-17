from django.urls import path
from .views import add_link, list_links

urlpatterns = [
    path('add/', add_link, name='add_link'),
path('list/', list_links, name='list_links'),
]
