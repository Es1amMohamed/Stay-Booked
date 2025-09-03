from django.db import models
from django.utils.text import slugify
from django.utils import timezone
import math
from django.db.models.signals import post_save
from django.dispatch import receiver



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
    

class Reservation(models.Model):
    COUNT = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="reservation_room")
    guest_name = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="reservation_guest")
    adults = models.IntegerField(choices=COUNT)
    children = models.IntegerField(choices=COUNT)
    check_in = models.DateField()
    check_out = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.room.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.room.name} - {self.guest_name}"
    
class HotelSubscriber(models.Model):
    guest_name = models.ForeignKey("accounts.CustomUser", on_delete=models.CASCADE, related_name="hotel_subscriber")
    hotel_name = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="hotel_subscribed")
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(null=True, blank=True)

    class Meta:
        verbose_name = "Hotel Subscriber"
        verbose_name_plural = "Hotel Subscribers"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.hotel_name.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.guest_name} - {self.hotel_name}"
    

@receiver(post_save, sender=Reservation)
def create_hotel_subscriber(sender, instance, created, **kwargs):
    if created:
        hotel = instance.room.hotel  
        HotelSubscriber.objects.get_or_create(
            guest_name=instance.guest_name,
            hotel_name=hotel
        )