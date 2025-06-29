from django import template

register = template.Library()

@register.filter
def calc_subtotal(price, quantity):
    try:
        return float(price) * int(quantity)
    except (ValueError, TypeError):
        return 0
