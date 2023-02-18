from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Explore(models.Model):
    explore_id = models.AutoField(primary_key=True)
    explore_title = models.CharField("Title of explore", max_length=32)
    explore_author = models.ForeignKey(User, verbose_name="Author of the Explore", on_delete=models.PROTECT)
    explore_date_created = models.DateTimeField("Date when the explore created", auto_now=False, auto_now_add=True)
    explore_description = models.TextField("Description of explore", max_length=256)