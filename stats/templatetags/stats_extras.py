from django import template
from stats.models import Character, Expedition, XP

register = template.Library()

def missionxp(char, ex):
    xp = XP.objects.all.filter(character=char).filter(expedition=ex)
    if xp.exists():
        return xp.value
    else:
        return ""

