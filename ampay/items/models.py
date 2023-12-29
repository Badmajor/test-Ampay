from django.db import models


class Discount(models.Model):
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


class Tax(models.Model):
    name = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=5, decimal_places=2)


class Item(models.Model):
    name = models.CharField(max_length=32)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(
        max_length=3,
        choices=(('usd', 'usd'), ('eur', 'eur')),
        default='usd'
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.name = f'order_{self.pk}'

    items = models.ManyToManyField(
        Item,
        through='OrderItem'
    )
    def get_all_items(self):
        return ((i.item, i.quantity) for i in OrderItem.objects.filter(order=self))

    def get_total_price(self):
        return sum(((i.item.price * i.quantity) for i in OrderItem.objects.filter(order=self)))

    @property
    def price(self):
        return self.get_total_price()

    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)


class OrderItem(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.DO_NOTHING
    )
    quantity = models.PositiveIntegerField(default=1)
    order = models.ForeignKey(
        Order,
        on_delete=models.DO_NOTHING
    )


