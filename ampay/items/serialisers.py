from django.urls import reverse
from rest_framework import serializers

from .utils import Product


class ItemSerializer(serializers.Serializer):
    session_id = serializers.SerializerMethodField()

    def get_session_id(self, obj):
        product = Product(obj)
        request = self.context.get('request')
        success_url = request.build_absolute_uri(
            location=reverse("items:detail", args=(obj.id,))
        )
        checkout_session = product.get_checkout_session(success_url)
        return checkout_session.id