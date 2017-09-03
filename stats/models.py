from django.db import models
import datetime
from django.utils import timezone

# 
class Player(models.Model):
    name = models.CharField(max_length=100)

    def priority(self):
        return 0

    def __str__(self):
        return self.name
    
class Character(models.Model):
    ACTIVE = 'AC'
    PROPOSED = 'PR'
    ONMISSION = 'OM'
    DEAD = 'DD'
    DEPARTED = 'DP'
    STATUS_CHOICE = (
        (ACTIVE, "Active"), 
        (PROPOSED, "Proposed"),
        (ONMISSION, "On Mission"),
        (DEAD, "Dead"),
        (DEPARTED, "Departed")
    )
    slug = models.SlugField()
    name = models.CharField(max_length=100)
    player = models.ForeignKey(Player)
    status = models.CharField(max_length=2, choices=STATUS_CHOICE, default=ACTIVE)
    dd_date = models.DateField(default=datetime.date.max)    

    def __str__(self):
        return self.name

    def level (self):
        return levelLookup(self.xp())
    
    def levelAt(self, time):
        return levelLookup(self.xpAt(time))

    def xpAt(self, time):
        x = 0
        xpobjs = XP.objects.all().filter(character=self).filter(expedition.date <= date)
        for xpo in xpobjs:
            x += xpo.value
        return x

    def xp (self):
        x = 0
        xpobjs = XP.objects.all().filter(character=self)
        for xpo in xpobjs:
            x += xpo.value
        return x

class Expedition(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    members = models.ManyToManyField(Character)
    
    dm = models.ForeignKey(Player)
    date = models.DateField()

    def __str__(self):
        return self.name

    def addMember (self, char, xp):
        t = XP(value=xp, character=char, expedition=self)
        t.save()
        self.members.add(char)
        self.save()

    def getMemberXP (self, char):
        return XP.objects.all().filter(expedition=self).filter(character=char).value

    def setMemberXP (self, char, xp):
        t = XP.objects.all().filter(expedition=self).filter(character=char)
        t.value = xp
        t.save()

    def updateStatus(self):
        st = ''
        if self.date < datetime.date.today(): st = Character.PROPOSED
        else: st = Character.ONMISSION
        for m in members: 
            m.status = st

class XP(models.Model):
    value = models.IntegerField()
    character = models.ForeignKey(Character)
    expedition = models.ForeignKey(Expedition)
    def __str__(self):
        return self.expedition.name + " (" + self.character.name + ")"

def levelLookup(xp):
    if (xp < 800): return 1
    elif (xp < 2400): return 2
    elif (xp < 4800): return 3
    elif (xp < 12000): return 4
    elif (xp < 24000): return 5
    elif (xp < 48000): return 6
    elif (xp < 96000): return 7
    elif (xp < 200000): return 8
    elif (xp < 300000): return 9
    elif (xp < 410000): return 10
    else: return 11
