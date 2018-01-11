# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from app01.models import *
import sys;

reload(sys);
sys.setdefaultencoding("utf8")


admin.site.register(classes)
admin.site.register(student)
admin.site.register(teacher)
admin.site.register(administrator)

# Register your models here.
