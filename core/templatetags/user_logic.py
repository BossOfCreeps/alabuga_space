from django import template

from core.models import Mission
from users.models import User

register = template.Library()


@register.filter
def get_mission_type(mission: Mission, user: User):
    if mission in user.missions.all():
        return "compiled"

    parent_missions = mission.as_child.values_list("parent_id", flat=True)
    if user.missions.filter(pk__in=parent_missions) or not parent_missions:
        return "open"

    return "locked"
