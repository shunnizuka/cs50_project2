from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max

from .models import User, Category, Bids, Listing


def index(request):

    listings = Listing.objects.filter(active=True)
    currentBids = {}
    print(listings)
    for listing in listings:
        maxBid = Bids.objects.filter(listing=listing.id).aggregate(Max('price'))
        if (maxBid['price__max'] == None):
            listing.currentBid = listing.bid
        else:
            listing.currentBid = maxBid['price__max']

    return render(request, "auctions/index.html", {
        "listings": listings,
        "currentBids": currentBids
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def createListing(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))

    if request.method == "POST":
        
        startingBid = float(request.POST["bid"])

        categoryFromdb = None;
        category = request.POST["category"]
        print(category)
        if category != 'None':
            categoryFromdb = Category.objects.get(pk=category)
        categoryInput = request.POST["categoryInput"]
        print(categoryInput)
        if categoryInput != None:
            newCategory = Category(category=categoryInput)
            newCategory.save()
            categoryFromdb = newCategory

        title = request.POST["title"]
        desc = request.POST["description"]
        image = request.POST["image"]

        if categoryFromdb != None:
            listing = Listing(user=request.user, category=categoryFromdb, title=title, description=desc, active=True, imageUrl=image, bid=startingBid)
        else:
            listing = Listing(user=request.user, title=title, description=desc, active=True, imageUrl=image, bid=startingBid)
        listing.save()

    return render(request, "auctions/createListing.html", {
        "categories": Category.objects.all()
    })