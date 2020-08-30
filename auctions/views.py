from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Max

from .models import User, Category, Bids, Listing, WatchList

def index(request):

    listings = Listing.objects.filter(active=True)
    currentBids = {}
    print(listings)
    for listing in listings:
        maxBid = Bids.objects.filter(listing=listing.id).aggregate(Max('price'))
        if (maxBid['price__max'] == None):
            listing.currentBid = round(listing.bid, 2)
        else:
            listing.currentBid = round(maxBid['price__max'], 2)

    return render(request, "auctions/index.html", {
        "listings": listings,
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
        if category != 'None':
            categoryFromdb = Category.objects.get(pk=category)
        categoryInput = request.POST["categoryInput"]
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

def watchlist(request):

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("index"))
    
    watchlistItems = WatchList.objects.filter(user=request.user.id)
    print(watchlistItems)
    for watchlist in watchlistItems:
        maxBid = Bids.objects.filter(listing=watchlist.listing).aggregate(Max('price'))
        if (maxBid['price__max'] == None):
            watchlist.listing.currentBid = round(watchlist.listing.bid, 2)
        else:
            watchlist.listing.currentBid = round(maxBid['price__max'], 2)

    print(watchlistItems)
    return render(request, "auctions/watchlist.html", {
        "watchlistItems": watchlistItems
    })

def categories(request):

    categoryList = Category.objects.all();
    return render(request, "auctions/categories.html",{
        "categories": categoryList
    })

def categoryListing(request, categoryId):

    listings = Listing.objects.filter(category=categoryId)
    return render(request, "auctions/index.html", {
        "listings": listings
    })

def listingPage(request, listingId):
    if request.method == "POST":
        # To place new bid
        if 'placeBid' in request.POST:
            bidPrice = float(request.POST["bid"])
            listing = Listing.objects.get(pk=listingId)
            newBid = Bids(user=request.user, listing=listing, price=bidPrice)
            newBid.save()
        return redirect('listingPage', listingId)
        
    else:
        listing = Listing.objects.get(pk=listingId)
        maxBid = Bids.objects.filter(listing=listing.id).aggregate(Max('price'))
        if (maxBid['price__max'] == None):
            listing.currentBid = round(listing.bid, 2)
        else:
            listing.currentBid = round(maxBid['price__max'], 2)
    
        isLister = False
        isWinner = False
        isInWatchlist = False
        userBid = 0

        if request.user.is_authenticated:
            isLister = True if listing.user == request.user else False
            watchlist = WatchList.objects.filter(user=request.user, listing=listingId)
            isInWatchlist = False if watchlist != None else True

            userBid = Bids.objects.filter(listing=listingId, user=request.user).aggregate(Max('price'))
            if (userBid['price__max'] == None):
                userBid = round(0, 2)
            else:
                userBid = round(userBid['price__max'], 2)

            if listing.active == False:
                bid = Bids.objects.filter(listing=listingId, price=listing.currentBid, user=request.user)
                isWinner = False if bid != None else True

        return render(request, "auctions/listing.html", {
            "listing": listing,
            "isLister": isLister,
            "isWinner": isWinner,
            "isInWatchlist": isInWatchlist,
            "userBid": userBid
        })
        