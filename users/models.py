from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, verbose_name='İsim Soyisim')
    company_name = models.CharField(max_length=300, verbose_name="Servis Adı")
    phone_number = models.CharField(
        max_length=11, verbose_name="Telefon Numarası")

    class Meta:
        verbose_name_plural = "Profiller"

    def __str__(self):
        return self.user.username


def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_profile(sender, instance, **kwargs):
    instance.profile.save()


# Profile
post_save.connect(create_profile, sender=User)
post_save.connect(save_profile, sender=User)
