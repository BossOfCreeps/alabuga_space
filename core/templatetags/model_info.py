from django import template

from core.models import Rank

register = template.Library()


@register.simple_tag(takes_context=True)
def get_user_theme(context):
    return context["request"].user.theme


@register.filter
def get_avatar(user):
    return Rank.objects.get(id=user.rank).image.url
