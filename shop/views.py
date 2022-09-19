from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from core import settings
from shop import models
from shop.payment import confirm_payment, payment
from shop.utils import snake_to_camel_in_dict


class ItemView(View):

    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        item = get_object_or_404(models.Item, pk=id)
        data = snake_to_camel_in_dict(item.as_dict_full())
        return render(request, 'item.html', {'data': data})


@method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        order_id = request.session.get('order_id')
        if order_id:
            order = get_object_or_404(models.Order, pk=order_id)
            data = snake_to_camel_in_dict(order.as_dict())
            return render(request, 'order.html', {'data': data, })

        return render(
            request,
            'message.html',
            context={'message': 'У тебя еще нет заказа', }
        )

    def post(self, request: HttpRequest) -> HttpResponse:
        order_id = request.session.get('order_id')
        item_id = request.POST.get('item_id')
        item = get_object_or_404(models.Item, pk=item_id)

        if not order_id:
            order = models.Order(order_currency=item.currency)
            order.save()
        else:
            order = models.Order.objects.get(pk=order_id)

        if item.currency != order.order_currency:
            return render(
                request,
                'message.html',
                context={'message': settings.ORDER_CURRENCY_ERROR, },
                status=400
            )

        item_from_order, created = models.OrderItems.objects.get_or_create(
            order=order, item=item)

        if not created:
            item_from_order.qty += 1
        item_from_order.save()

        if not order_id:
            request.session['order_id'] = order.id

        data = snake_to_camel_in_dict(order.as_dict())
        return render(request, 'order.html', {'data': data}, status=201)


class OrderItemView(View):

    def delete(self, request: HttpRequest, id: int) -> HttpResponse:
        deleted_order_item = models.OrderItems.objects.filter(id=id).first()
        order = deleted_order_item.order
        deleted_order_item.delete()
        another_order_items = (models.OrderItems.objects.
                               filter(order=order).first())
        if not another_order_items:
            order.delete()
            request.session['order_id'] = None
        return render(
                request,
                'message.html',
                context={'message': 'Товар удален', },
                status=204
            )


class BuyView(View):

    def get(self, request: HttpRequest) -> HttpResponse:
        id = request.session.get('order_id')
        if not id:
            return render(
                request,
                'message.html',
                context={'message': 'У тебя еще нет заказа', },
                status=404
            )

        order = models.Order.objects.get(pk=id)
        order_price_detail = order.as_dict().get('order_price_detail')

        amount = order_price_detail.get('order_final_price')

        payment_intent_id = payment(amount, order.order_currency)
        context = {
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'payment_intent_id': payment_intent_id,
        }
        return render(request, 'payment.html', context)

    def post(self, request: HttpRequest) -> HttpResponse:
        payment_intent_id = request.POST.get('payment_intent_id')
        payment_method_id = request.POST.get('payment_method_id')
        message = confirm_payment(payment_intent_id, payment_method_id)
        if message != 'Что-то пошло не так':
            request.session['order_id'] = None
        return render(request, 'message.html', context={'message': message, })
