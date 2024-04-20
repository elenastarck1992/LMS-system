import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    """Функция создания продукта в Stripe"""

    title_product = f'{instance.paid_course}' if instance.paid_course else f'{instance.paid_lesson}'
    stripe_product = stripe.Product.create(name=f'{title_product}')
    return stripe_product['id']


def create_stripe_price(product, id):
    """Функция создания цены в Stripe"""
    stripe_price = stripe.Price.create(
        currency='rub',
        unit_amount=product.payment_sum * 100,
        product=id,
    )
    return stripe_price['id']


def create_stripe_session(stripe_price_id):
    """Функция создания сессии в Stripe"""
    stripe_session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": stripe_price_id, "quantity": 1}],
        mode="payment",
    )
    return stripe_session['url'], stripe_session['id']
