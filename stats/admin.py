from django.contrib import admin
from .models import Player
from .models import Character 
from .models import Expedition
from .models import XP

# Register your models here.
admin.site.register(Player)
admin.site.register(Character)
admin.site.register(Expedition)
admin.site.register(XP)
