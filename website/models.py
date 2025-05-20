from django.db import models
from django.utils.text import slugify


class Config(models.Model):
    contact_phone = models.CharField(max_length=100, blank=True, null=True, default='+38162227054')
    email = models.EmailField(blank=True, null=True, default='contact@miyamie.com')
    instagram_link = models.CharField(max_length=255, blank=True, null=True, default='www.instagram.com')
    facebook_link = models.CharField(max_length=255, blank=True, null=True, default='www.facebook.com')
    tiktok_link = models.CharField(max_length=255, blank=True, null=True, default='www.tiktok.com')
    address = models.CharField(max_length=255, blank=True, null=True, default='defautl address')


class Appointment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time}"


class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Category(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand.name} - {self.name}"


class Dress(models.Model):
    TAG_CHOICES = [
        ('new', 'New'),
        ('bestseller', 'Bestseller'),
        ('sale', 'Sale'),
    ]

    slug = models.SlugField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='dresses')
    name = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    description = models.TextField()
    additional_info = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True, null=True)
    home_page = models.IntegerField(default=0)
    main_image = models.ImageField(upload_to='dresses/main/')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class DressImage(models.Model):
    dress = models.ForeignKey(Dress, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='dresses/extra/')

    def __str__(self):
        return f"Image for {self.dress.name}"
