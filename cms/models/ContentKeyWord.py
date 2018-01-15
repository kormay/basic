from django.db import models
from .Base import Base
from .KeyWord import KeyWord
from .Content import Content


class ContentKeyWord(Base):
    key_word = models.ForeignKey(KeyWord,on_delete=models.CASCADE)
    content = models.ForeignKey(Content,on_delete=models.CASCADE)