from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.user}: {self.price}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user}: {self.comment}"

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    active = models.BooleanField()
    imageUrl = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Lister")
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="highestBid") 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, related_name="listingCategory")
    comments = models.ManyToManyField(Comments, blank=True, related_name="ListingComments")

    def __str__(self):
        return f"{self.title}: {self.description}, Lister: {self.user}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="WatchlistUser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="WatchlistListing")

    def __str__(self):
        return f"{self.user}: {self.listing}"
