from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete, post_save
from django.dispatch.dispatcher import receiver
from PIL import Image as PILImage
from django.core.validators import MaxValueValidator, MinValueValidator
import magic
from django.core.exceptions import ValidationError


class Tier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    tier = models.ForeignKey(Tier, on_delete=models.SET_NULL, null=True, default=None)
    def __str__(self):
        return self.username


def validate_image(image):
    filetype = magic.from_buffer(image.read())
    print("BBBBBBBBBBBBBBBBBBBBBBBBB")
    print(filetype)
    if "PNG" in filetype or "JPEG" in filetype:
        return image
    raise ValidationError("File is not PNG or JPG.")
    

class Image(models.Model):
    owner       = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image       = models.ImageField(upload_to='images/', blank=False, validators=[validate_image])
    thumb200    = models.ImageField(upload_to='images/thumbnails200/', blank=True)
    thumb400    = models.ImageField(upload_to='images/thumbnails400/', blank=True)
    binary      = models.ImageField(upload_to='images/binary/', blank=True)

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
    img = cv2.imread(instance.image.url[1::], 2)
    ret, bw_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
    cv2.imwrite(f'media/binary/binary{instance.id}.jpg', bw_img)

    Image.objects.filter(id=instance.id).update(
            thumb200=f'thumbnails_200/200Thumbnail{instance.id}.png',
            thumb400=f'thumbnails_400/400Thumbnail{instance.id}.png',
            binary=f'binary/binary{instance.id}.jpg'
    )

@receiver(pre_delete, sender=Image)
def media_images_delete(sender, instance, **kwargs):
    instance.image.delete(False)
    if instance.thumb200:
        instance.thumb200.delete(False)
    if instance.thumb400:
        instance.thumb400.delete(False)
    if instance.binary:
        instance.binary.delete(False)


class Link(models.Model):
    image       = models.ForeignKey(Image, related_name='links', on_delete=models.CASCADE)
    duration    = models.IntegerField(blank=False, validators=[MaxValueValidator(30000),MinValueValidator(300)])
    url         = models.CharField(max_length=250)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url



