# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class classes(models.Model):
    caption=models.CharField(max_length=64)
    def __str__(self):
        return self.caption

class student(models.Model):
    name=models.CharField(max_length=16)
    age=models.CharField(max_length=8)
    email=models.CharField(max_length=16,default=None)
    caption=models.ForeignKey("classes")
    def __str__(self):
        return self.name

class teacher(models.Model):
    name=models.CharField(max_length=16)
    classes=models.ManyToManyField("classes")
    def __str__(self):
        return self.name

class administrator(models.Model):
    user=models.CharField(max_length=64)
    passwd=models.CharField(max_length=64)
    def __str__(self):
        return self.user

# Create your models here.
