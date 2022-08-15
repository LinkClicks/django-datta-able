# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tokens(models.Model):
    access_token = models.CharField(max_length=150,)
    refresh_token = models.CharField(max_length=100,)
