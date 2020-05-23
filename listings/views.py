from django.shortcuts import render , get_object_or_404
from django.core.paginator import Paginator
from django.contrib import humanize
from django.http import HttpResponse
from .models import Listing
from .choices import bedroom_choices, state_choices, price_choices


def index(request):
   listings = Listing.objects.order_by('-list_date').filter(is_published = True)
  
   paginator = Paginator(listings, 6)
   page = request.GET.get('page')
   paged_listings = paginator.get_page(page) 
   
   context = {
       'listings': paged_listings
   }
  
   return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

def search(request):
    listings_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            listings_list = listings_list.filter(description__icontains=keywords)
    
    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            listings_list = listings_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            listings_list = listings_list.filter(state__iexact=state)

    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            listings_list = listings_list.filter(bedrooms__lte=bedrooms)

    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            listings_list = listings_list.filter(price__lte=price)


    context = {
        'listings_list': listings_list,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context)
