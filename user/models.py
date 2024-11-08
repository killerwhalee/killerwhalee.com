from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from core.utils import uuid_filepath


class UserManager(BaseUserManager):
    """
    Custom User Manager

    """

    use_in_migrations = True

    def create_user(self, email, password=None):
        user = self.model(email=email)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)

        # Set admin permissions
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model

    This user model is designed for simplification.

    """

    objects = UserManager()

    # User email is used as primary key
    email = models.EmailField(
        "User email",
        max_length=254,
        primary_key=True,
    )

    # Basic permissions overwritten
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"


class Profile(models.Model):
    """
    Extended User Profile Model

    This model provided additional information of user.

    """

    # User reference
    user = models.OneToOneField("user.User", on_delete=models.CASCADE)

    # profile informations
    image = models.ImageField("profile image", upload_to=uuid_filepath, null=True)
    name = models.CharField("profile name", max_length=16)

    def __str__(self) -> str:
        return f"Profile ({self.user})"


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        name, _ = instance.email.split("@")

        Profile.objects.create(user=instance, name=name)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
