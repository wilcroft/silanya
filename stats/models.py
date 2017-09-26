from django.db import models
import datetime
from django.utils import timezone
from markdownx.models import MarkdownxField

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

    def xpAt(self, date):
        x = 0
        xpobjs = XP.objects.all().filter(character=self)
        xpobjs = xpobjs.filter(expedition__date__lte = date)
        for xpo in xpobjs:
            x += xpo.value
        return x

    def xpSince(self, date):
        x = 0
        xpobjs = XP.objects.all().filter(character=self)
        xpobjs = xpobjs.filter(expedition__date__gte = date)
        for xpo in xpobjs:
            x += xpo.value
        return x

    def xp (self):
        x = 0
        xpobjs = XP.objects.all().filter(character=self)
        for xpo in xpobjs:
            x += xpo.value
        for cxp in CXP.objects.filter(character=self):
            x += cxp.getValue()
        return x

    def xpByEx(self):
        lst = []
        for ex in Expedition.objects.order_by('-date'):
            if ex.members.filter(slug=self.slug).exists():
                lst.append(ex.getMemberXP(self))
            else:
                lst.append("")
        return lst

    def tableInfo(self):
        sdict = dict(Character.STATUS_CHOICE)
        lst = []
        lst.append(sdict[self.status])
        lst.append(levelLookup(self.xp()))
        lst.append(self.xp())
        lst.append(nextLevel(self.xp()))
        lst.extend(self.xpByEx())
        return lst

class Expedition(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    members = models.ManyToManyField(Character)
    
    dm = models.ForeignKey(Player)
    date = models.DateField()
    
    log = MarkdownxField()

    def __str__(self):
        return self.name

    def addMember (self, char, xp):
        t = XP(value=xp, character=char, expedition=self)
        t.save()
        self.members.add(char)
        self.save()

    def getMemberXP (self, char):
#        return XP.objects.all().filter(expedition=self).filter(character=char).value
        return XP.objects.get(expedition=self,character=char).value

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
    def getValue(self):
        return self.value

class CXP(models.Model):
    lumpNotPool = models.BooleanField()
    value = models.IntegerField()
    character = models.ForeignKey(Character)
    expedition = models.ForeignKey(Expedition)
    
    def __str__(self):
        return self.expedition.name + " (" + self.character.name + ")"
    
    def getValue(self):
        if (self.lumpNotPool): return self.value
        else: 
            xp = self.character.xpSince(self.expedition.date)
            if (xp > self.value): return self.value
            else: return xp

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

def nextLevel(xp):
    lvl = levelLookup(xp)
    if (lvl == 1): return 800-xp
    elif lvl == 2: return 2400 - xp
    elif lvl == 3: return 4800 - xp
    elif lvl == 4: return 12000 - xp
    elif lvl == 5: return 24000 - xp
    elif lvl == 6: return 48000 - xp
    elif lvl == 7: return 96000 - xp
    elif lvl == 8: return 200000 - xp
    elif lvl == 9: return 300000 - xp
    elif lvl == 10: return 410000 - xp
    else: return -1
