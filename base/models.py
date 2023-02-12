from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from PIL import Image as PILImage




class Tier(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, default=None)

    def __str__(self):
        return self.username


class Image(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=False)
    thumb200 = models.ImageField(upload_to='images/thumbnails200/', blank=True)
    thumb400 = models.ImageField(upload_to='images/thumbnails400/', blank=True)

    def __str__(self):
        return "image" + " " + self.owner.username + " " + str(self.id)

@receiver(post_save, sender=Image)
def create_thumbnails(sender, instance, **kwargs):
    image = PILImage.open(instance.image.url[1::])
    image.thumbnail((200, 200))
    image.save(f'media/thumbnails_200/200Thumbnail{instance.id}.png')
    image = PILImage.open(instance.image.url[1::])
    image.thumbnail((400, 400))
    image.save(f'media/thumbnails_400/400Thumbnail{instance.id}.png')

    Image.objects.filter(id=instance.id).update(
            thumb200=f'thumbnails_200/200Thumbnail{instance.id}.png',
            thumb400=f'thumbnails_400/400Thumbnail{instance.id}.png'
    )

@receiver(pre_delete, sender=Image)
def media_images_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    if instance.thumb200:
        instance.thumb200.delete(False)
    if instance.thumb400:
        instance.thumb400.delete(False)



