from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('host', 'host'),
        ('guest', 'guest'),
    )
    role = models.CharField(choices=ROLE_CHOICES, default='guest', max_length=32)
    phone_number = PhoneNumberField()
    avatar = models.ImageField(upload_to='avatar_user/', null=True, blank=True)

    def __str__(self):
        return f'{self.username} {self.email}'


class Country(models.Model):
    country_name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.country_name

class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=64)

    def __str__(self):
        return self.city_name

class Rules(models.Model):
        RULES_CHOICES = (
            ('no_smoking', 'no_smoking'),
            ('pets_allowed', 'pets_allowed'),
            ('no_parties', 'no_parties'),
            ('quiet_hours', 'quiet_hours'),
            ('children_allowed', 'children_allowed'),
        )
        rule = models.CharField(choices=RULES_CHOICES, max_length=32)

        def __str__(self):
            return self.rule

class Property(models.Model):
    PROPERTY_CHOICES = (
        ('apartment', 'apartment'),
        ('house', 'house'),
        ('studio', 'studio'),
        ('townhouse', 'townhouse'),
        ('villa', 'villa'),
        ('cottage', 'cottage'),
    )

    title = models.CharField(max_length=250)
    description = models.TextField()
    price_per_night = models.PositiveSmallIntegerField()
    city = models.ForeignKey(City,on_delete=models.CASCADE)
    country = models.ForeignKey(Country,on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    property_type = models.CharField(choices=PROPERTY_CHOICES, max_length=32)
    max_guests = models.PositiveSmallIntegerField()
    bedrooms = models.PositiveSmallIntegerField()
    bathrooms = models.PositiveSmallIntegerField()
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='properties')
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    rules = models.ForeignKey(Rules,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.city}'

    def get_avg_rating(self):
        ratings = self.reviews_property.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 2)
        return 0

    def get_count_review(self):
        self.reviews_property.count()


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_image/')


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'pending'),
        ('approved', 'approved'),
        ('rejected', 'rejected'),
        ('cancelled', 'cancelled'),
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings_property')
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='bookings_guests')
    check_in = models.DateField()
    check_out = models.DateField()
    status = models.CharField(choices=STATUS_CHOICES, max_length=16, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.check_in}  {self.check_out}'


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews_property')
    guest = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews_guests')
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.comment} {self.rating}'


class Amenity(models.Model):
    name = models.CharField(max_length=64)
    image = models.CharField(max_length=64, blank=True, null=True)
    property = models.ManyToManyField(Property, related_name='amenity_property', blank=True)

    def __str__(self):
        return self.name