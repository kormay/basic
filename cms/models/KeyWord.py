from django.db import models
from .Base import Base

class KeyWord(Base):
    word = models.CharField(max_length=100)