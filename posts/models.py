from django.db import models
import qrcode
import qrcode.image.svg
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Process(models.Model):
    process = models.CharField(max_length=200, verbose_name='Yapılan işlemler')
    price = models.PositiveIntegerField(verbose_name="Fiyat")
    number = models.PositiveIntegerField(verbose_name="Adet", default=1)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return self.process

    class Meta:
        ordering = ['process']

    def total_price(self):
        return self.number * self.price


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    full_name = models.CharField(max_length=100, verbose_name="İsim Soyisim")
    company_name = models.CharField(
        max_length=100, blank=True, null=True, verbose_name="Servis Adı")
    phone_number = models.CharField(
        blank=True, null=True, max_length=11, verbose_name="Telefon Numarası")
    brand = models.CharField(max_length=100, verbose_name="Marka")
    model = models.CharField(max_length=100, verbose_name="Model")
    error = models.TextField(verbose_name="Arızalar")
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    action = models.ManyToManyField(Process, blank=True)
    mission = models.BooleanField(default=False)
    come = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    date = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturulma Tarihi")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        qr_code_img = qrcode.make(self.full_name + "\n" + self.company_name + "\n"+self.brand + "-" + self.model + "\n" + str(self.phone_number) + "\n" +
                                  "http://127.0.0.1:8000/posts/pdf/" + str(self.id))
        w, h = qr_code_img.size
        qr_code_img = qr_code_img.resize((300, 300), Image.ANTIALIAS)
        canvas = Image.new(
            'RGB', (570, 370), "white")
        space = (135, 35)
        canvas.paste(qr_code_img, space)
        font = ImageFont.truetype(font='arial.ttf', size=30)
        ImageDraw.Draw(canvas).text((20, 10), self.brand + " " + "self.full_name",
                                    font=font, fill="black")
        fname = f'{self.full_name + " " +self.brand + " " + self.model}.png'
        buffer = BytesIO()

        canvas.rotate(0, expand=True).save(buffer, 'PNG')

        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()

        super().save(*args, **kwargs)
