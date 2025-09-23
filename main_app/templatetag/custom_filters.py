from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiply two numbers"""
    return value * arg
