from django.views.generic import DetailView
from rest_framework import generics

from .models import Item
from .serialisers import ItemSerializer


class ItemDetail(DetailView):
    model = Item


class ItemBuyAPI(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer