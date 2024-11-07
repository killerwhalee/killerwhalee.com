from django.db import models


class FunFact(models.Model):
    fact = models.TextField("Fun fact")
