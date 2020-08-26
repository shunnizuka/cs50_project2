from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField()
    description = models.CharField()
    active = models.BooleanField()
    imageUrl = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="Lister")
    bid = models.ForeignKey(Bids, on_delete=models.CASCADE, related_name="highestBid") 
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listingCategory")

    def __str__(self):
        return f"{self.title}: {self.description}, Lister: {self.user}"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    price = models.DecimalField(decimal_places=2)

    def __str__(self):
        return f"{self.user}: {self.price}"

class Comments(models.Model):
    comment = models.CharField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listingComment")

    def __str__(self):
        return f"{self.listing}: {self.comment}"

class Category(models.Model):
    category = models.CharField()

    def __str__(self):
        return f"{self.category}"

class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="WatchlistUser")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="WatchlistListing")

    def __str__(self):
        return f"{self.user}: {self.listing}"
