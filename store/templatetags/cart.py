# templatetags/cart.py

from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == product.id:
            return cart.get(id)
    return 0

@register.filter(name='price_total')
def price_total(product, cart):
    return product.price * cart_quantity(product, cart)

@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum = 0
    for p in products:
        sum += price_total(p, cart)
    return sum
