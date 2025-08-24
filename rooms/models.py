from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import math


class Hotel(models.Model):
    name = models.CharField(unique=True,max_length=100)
    image = models.ImageField(upload_to="hotel/")
    description = models.TextField(max_length=10000)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=True, blank=True)

    @property
    def room_count(self):
        return self.room_hotel.count()
    
    @property
    def avg_price(self):

        avg = self.room_hotel.aggregate(models.Avg("price"))["price__avg"] or 0
        return math.ceil(avg)
    class Meta:
        ordering = ["name"]
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Room(models.Model):
    name = models.CharField(unique=True,max_length=100)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="room_hotel")
    capacity = models.IntegerField(default=2)
    image = models.ImageField(upload_to="room/")
    price = models.IntegerField(default=0)
    description = models.TextField(max_length=10000)
    availability = models.BooleanField(default=True)
    category = models.ForeignKey(
        "Category", related_name="room_category", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(unique=True,max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name