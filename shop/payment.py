import stripe

from core.settings import API_KEY

stripe.api_key = API_KEY


def payment(amount: int, order_currency: str) -> int:
    payment_intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=order_currency,
        payment_method_types=['card', ],
    )
    return payment_intent.id


def confirm_payment(payment_intent_id: str, payment_method_id: str) -> str:
    try:
        response = stripe.PaymentIntent.confirm(
            payment_intent_id,
            payment_method=payment_method_id
        )
        return ('Твой <a href="'
                + response['charges']['data'][0]['receipt_url']
                + '">чек</a>')
    except Exception:
        return 'Что-то пошло не так'
