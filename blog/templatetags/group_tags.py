from django import template

register = template.Library()


@register.simple_tag
def in_group(user, group_name):
    """Return True if user is staff or belongs to the named group."""
    if not user or not getattr(user, 'is_authenticated', False):
        return False
    if getattr(user, 'is_staff', False):
        return True
    return user.groups.filter(name=group_name).exists()
