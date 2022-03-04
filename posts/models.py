from django.db import models
from django.core.validators import MinLengthValidator
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class Post(models.Model):
    name = models.CharField(
            max_length=200,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    description = models.TextField(
        max_length=400,
        validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )
    #owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    options = (
        ('sell', "Sell"),
        ('rent', "Rent"),
        ('exchange', "Exchange"),
    )
    option = models.CharField(max_length=10, choices=options, default="Rent")
    categories = (
        ('textbook', "Textbook"),
        ('tech', "Tech"),
        ('sport', "Sport"),
        ('furniture', "Furniture"),
        ('other', "Other"),
    )
    category = models.CharField(max_length=10, choices=categories, default="Textbook")
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    location = models.CharField(
            max_length=50,
            validators=[MinLengthValidator(2, "Title must be greater than 2 characters")]
    )


    # Picture
    picture = models.ImageField(null=True, editable=True)
    #content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file')

    # Shows up in the admin list
    def __str__(self):
        return self.name