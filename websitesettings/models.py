from django.db import models



class Settings(models.Model):
    site_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="home_page/")
    email = models.EmailField(max_length=254)
    image = models.ForeignKey(
        "Image",
        related_name="home_page_image",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(max_length=20)
    description = models.TextField(max_length=1000)
    address = models.CharField(max_length=500, default="Egypt")
    fb_link = models.URLField(max_length=200, null=True, blank=True)
    tw_link = models.URLField(max_length=200, null=True, blank=True)
    in_link = models.URLField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=300, default="Egypt")

    def __str__(self):
        return self.site_name
    

class Image(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=250)
    image = models.ImageField(upload_to="home_page/")

    def __str__(self):
        return self.title


class Services(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=200)
    image = models.ImageField(upload_to="services/", null=True, blank=True)
    description = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name
