from statistics import mode
from unicodedata import name
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.conf import settings
import json
from datetime import date

from .base import model_helper as base


class Document(base.BaseModel):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

### PRODUCT SESSION