from typing import Union

from decouple import config
import stripe

from .models import Item, Order


class Product:

    def __init__(self, obj: Union[Item, Order], quantity=1):
        stripe.api_key = config('SECRET_KEY_STRIPE')
        self.obj = obj
        self.quantity = quantity
        self.amount = obj.price * 100
        self.product = self.create_or_get_product()
        self.price = self.create_price()
        self.tax_rate = self.create_or_get_tax_rate()
        self.discount = self.create_or_get_discount()
        self.currency = getattr(obj, 'currency', 'usd')

    def create_or_get_product(self):
        product_id = f'{self.obj.__class__.__name__}_{self.obj.pk}'
        try:
            product = stripe.Product.retrieve(product_id)
        except stripe._error.InvalidRequestError:
            product = stripe.Product.create(
                name=self.obj.name,
                id=product_id,
            )
        return product

    def create_price(self):
        return stripe.Price.create(
            currency='usd',
            unit_amount=self.amount,
            product=self.product.id
        )

    def create_or_get_tax_rate(self):
        if hasattr(self.obj, 'tax') and (tax := self.obj.tax):
            tax_id = f'trx_{tax.pk}'
            try:
                tax_rate = stripe.TaxRate.retrieve(tax_id)
            except stripe._error.InvalidRequestError:
                tax_rate = stripe.TaxRate.create(
                    id=tax_id,
                    display_name=tax.name,
                    inclusive=False,
                    percentage=tax.rate,
                )
            return tax_rate
        return None

    def create_or_get_discount(self):
        if hasattr(self.obj, 'discount') and (discount := self.obj.discount):
            discount_id = f'dst_{discount.pk}'
            try:
                discount = stripe.Coupon.retrieve(discount_id)
            except stripe._error.InvalidRequestError:
                discount = stripe.Coupon.create(
                    id=discount_id,
                    amount_off=discount.amount,
                    currency='usd',
                )
            return discount
        return None



    def get_checkout_session(self, success_url='http://127.0.0.1:8000/'):
        line_items_dict = {
            'price': self.price.id,
            'quantity': self.quantity,
        }
        if hasattr(self.tax_rate, 'id'):
            tax_rate_id = self.tax_rate.id
            line_items_dict['tax_rates'] = (tax_rate_id,)
        discount = None
        if hasattr(self.discount, 'id'):
            discount = self.discount.id

        checkout_session = stripe.checkout.Session.create(
            success_url=success_url,
            line_items=[line_items_dict],
            mode="payment",
            currency='usd',
            discount = discount


        )
        return checkout_session

    def get_payment_intent(self):
        payment_intent = stripe.PaymentIntent.create(
            amount=self.amount,
            currency="usd",
            automatic_payment_methods={"enabled": True},
        )
        return payment_intent
