from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}: {self.comment}"

class Category(models.Model):
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    imageUrl = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Lister")
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.OneToOneField(Category, on_delete=models.CASCADE, blank=True, related_name="listingCategory")
    comments = models.ManyToManyField(Comments, blank=True, related_name="ListingComments")

    def __str__(self):
        return f"{self.title}: {self.description}, Lister: {self.user} Price: {self.bid} image: {self.imageUrl}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="WatchlistUser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="WatchlistListing")

    def __str__(self):
        return f"{self.user}: {self.listing}"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_bid")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.user}: {self.price} for {self.listing}"
