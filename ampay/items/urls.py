from django.urls import path

from . import views

app_name = 'items'

urlpatterns = [
    path('item/<int:pk>/', views.ItemDetail.as_view(), name='detail'),
    path('buy/<int:pk>/', views.ItemBuyAPI.as_view(), name='buy'),
]
