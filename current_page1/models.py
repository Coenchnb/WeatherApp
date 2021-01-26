from typing import re

from django.db import models
from django import forms


# Create your models here.

class city_form(forms.Form):
    city_name = (forms.CharField(max_length=100, label=""))

    def __repr__(self):
        return repr(self.city_name)



