from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact


def contact(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        realtor_id = request.POST['realtor_id']
        listing = request.POST['listing']
        listing_id = request.POST['listing_id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

    # Check if user already submitted listing
    if request.user.is_authenticated:
        if Contact.objects.filter(listing_id=listing_id, user_id=user_id).exists():
            messages.error(request, 'You have already made an inquiry for this listing')
            return redirect('/listings/'+listing_id)

    # Save to DB
    c = Contact(listing=listing, listing_id=listing_id, name=name,
            email=email, phone=phone, message=message, user_id=user_id)
    c.save()

    # Send email
    send_mail(
        'Property Listing Inquiry',
        'There has been an inquiry for' + listing + '. Sign into the admin panel for more',
        'test@gmail.com',
        [realtor_email],
        fail_silently=False,
    )

    messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
    return redirect('/listings/'+listing_id)
