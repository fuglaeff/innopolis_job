from typing import Any, Dict, List, Union

from django.db import models

from shop.validators import discount_and_tax_validator

CURRENCY_CHOISE = (
    ('rub', 'ruble',),
    ('usd', 'dollar',),
)


class Item(models.Model):
    name = models.CharField(verbose_name='Product name', max_length=25)
    description = models.CharField(
        verbose_name='Product description', max_length=255)
    price = models.IntegerField(
        verbose_name='Product price')
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOISE)

    @property
    def all_taxes(self) -> List[Dict[str, Union[str, int]]]:
        taxes_list = [tax.as_dict() for tax in self.taxes.all()]

        if taxes_list == []:
            return []

        for i, tax in enumerate(taxes_list):
            tax_sum = self.price * tax.get('val', 0) / 100
            taxes_list[i].update(
                {'tax_sum': int(tax_sum)})

        return taxes_list

    @property
    def all_discounts(self) -> List[Dict[str, Union[str, int]]]:
        discounts_list = [disc.as_dict() for disc in self.discount.all()]

        if discounts_list == []:
            return []

        price_with_discount = self.price
        for i, disc in enumerate(discounts_list):
            discount = price_with_discount * disc.get('val', 0) / 100
            price_with_discount *= (1 - disc.get('val', 0) / 100)
            discounts_list[i].update(
                {'discount_sum': int(discount)})

        return discounts_list

    @property
    def price_detail(self) -> Dict[str, int]:
        taxes_sum = discount_sum = 0

        for tax in self.all_taxes:
            taxes_sum += tax.get('tax_sum', 0)

        for disc in self.all_discounts:
            discount_sum += disc.get('discount_sum', 0)

        return {
            'tax_all_sum': taxes_sum,
            'tax_all_val': int(taxes_sum / self.price),
            'disc_all_sum': discount_sum,
            'disc_all_val': int(discount_sum / self.price),
            'final_price': self.price - discount_sum + taxes_sum,
        }

    def as_dict(self) -> Dict[str, Union[str, int]]:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'currency': self.currency,
        }

    def as_dict_full(self) -> Dict[str, Union[str, int, Dict[str, int]]]:
        object_dict = self.as_dict()
        object_dict.update(
            {
                'discounts': self.all_discounts,
                'taxes': self.all_taxes,
                'price_detail': self.price_detail,
            }
        )
        return object_dict


class Discount(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='discount'
    )
    discount_name = models.CharField(
        verbose_name='Discount name', max_length=25)
    val = models.IntegerField(
        validators=[discount_and_tax_validator]
    )

    def as_dict(self) -> Dict[str, Union[str, int]]:
        return {
            'discount_id': self.id,
            'discount_name': self.discount_name,
            'val': self.val,
        }

    class Meta:
        ordering = ('-val',)


class Tax(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='taxes'
    )
    tax_name = models.CharField(
        verbose_name='Tax name', max_length=25)
    val = models.IntegerField(
        validators=[discount_and_tax_validator]
    )

    def as_dict(self) -> Dict[str, Union[str, int]]:
        return {
            'discount_id': self.id,
            'tax_name': self.tax_name,
            'val': self.val,
        }


class Order(models.Model):
    order_currency = models.CharField(max_length=3, choices=CURRENCY_CHOISE)
    is_complite = models.BooleanField(default=False)

    @property
    def all_order_items(self) -> Dict[str, Any]:
        order_items = []
        for item in self.items.all():
            order_item_dict = {
                'order_item_id': item.id,
                'qty': item.qty,
                'item': item.item.as_dict_full(),
            }
            order_items.append(order_item_dict)

        return order_items

    def as_dict(self) -> Dict[str, Any]:
        all_price = all_discount = all_tax = 0

        for item in self.all_order_items:
            item_price_detail = item['item'].get('price_detail')
            qty = item.get('qty')
            all_price += item_price_detail.get('final_price') * qty
            all_discount += item_price_detail.get('disc_all_sum') * qty
            all_tax += item_price_detail.get('tax_all_sum') * qty

        order_tax_all_val = int(all_tax * 100 / (all_price + all_discount))
        order_disc_all_val = int(all_discount *
                                 100 / (all_price + all_discount))

        return {
            'order_id': self.id,
            'items': self.all_order_items,
            'order_currency': self.order_currency,
            'order_price_detail': {
                'order_old_price': all_price + all_discount,
                'order_tax_all_sum': all_tax,
                'order_tax_all_val': order_tax_all_val,
                'order_disc_all_sum': all_discount,
                'order_disc_all_val': order_disc_all_val,
                'order_final_price': all_price,
            }
        }


class OrderItems(models.Model):
    item = models.ForeignKey(
        to=Item,
        on_delete=models.CASCADE,
        related_name='order'
    )
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    qty = models.IntegerField(default=1)
