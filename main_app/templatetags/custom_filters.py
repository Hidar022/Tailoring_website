from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    """Multiply two numbers"""
    return value * arg


@register.filter
def image_url(image_field):
    """Return a usable image URL.

    If the ImageField stores an absolute URL (starts with http), return it directly.
    Otherwise, fall back to the field's `.url` property (which uses storage).
    If anything fails, return an empty string.
    """
    try:
        name = getattr(image_field, 'name', '') or ''
        if isinstance(name, str) and name.lower().startswith('http'):
            return name
        return image_field.url
    except Exception:
        return ''
