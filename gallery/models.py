from django.db import models
from django.contrib.auth.models import User

from _config.utils import uuid_filepath

# Create your models here.
class Explore(models.Model):
    explore_id = models.AutoField(primary_key=True)
    explore_title = models.CharField("Title of explore", max_length=32)
    explore_author = models.ForeignKey(User, verbose_name="Author of the Explore", on_delete=models.PROTECT)
    explore_date_created = models.DateTimeField("Date when the explore created", auto_now=False, auto_now_add=True)
    explore_description = models.TextField("Description of explore", max_length=256)
    explore_cover_image = models.ImageField("Cover image of explore", upload_to=uuid_filepath, max_length=None, null=True)