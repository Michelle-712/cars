from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Property, Agent, ContactMessage


def index(request):
    featured_properties = Property.objects.filter(is_featured=True, status='available')[:6]
    latest_properties = Property.objects.filter(status='available').order_by('-created_at')[:6]
    agents = Agent.objects.all()[:4]

    context = {
        'featured_properties': featured_properties,
        'latest_properties': latest_properties,
        'agents': agents,
    }
    return render(request, 'index.html', context)


def about(request):
    agents = Agent.objects.all()

    context = {
        'agents': agents,
    }
    return render(request, 'about.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message,
            )
            messages.success(request, 'Your message has been sent successfully. We will get back to you soon!')
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'contact.html')


def properties(request):
    properties_list = Property.objects.filter(status='available')

    # Filtering
    property_type = request.GET.get('property_type')
    listing_type = request.GET.get('listing_type')
    city = request.GET.get('city')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    bedrooms = request.GET.get('bedrooms')

    if property_type:
        properties_list = properties_list.filter(property_type=property_type)
    if listing_type:
        properties_list = properties_list.filter(listing_type=listing_type)
    if city:
        properties_list = properties_list.filter(city__icontains=city)
    if min_price:
        properties_list = properties_list.filter(price__gte=min_price)
    if max_price:
        properties_list = properties_list.filter(price__lte=max_price)
    if bedrooms:
        properties_list = properties_list.filter(bedrooms=bedrooms)

    context = {
        'properties': properties_list,
    }
    return render(request, 'properties.html', context)


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    related_properties = Property.objects.filter(
        city=property.city,
        status='available'
    ).exclude(pk=pk)[:3]

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        message = request.POST.get('message')

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=f'Enquiry about: {property.title}',
                message=message,
                property=property,
            )
            messages.success(request, 'Your enquiry has been sent! An agent will contact you shortly.')
            return redirect('property_detail', pk=pk)
        else:
            messages.error(request, 'Please fill in all required fields.')

    context = {
        'property': property,
        'related_properties': related_properties,
    }
    return render(request, 'property_detail.html', context)


def agents(request):
    agents_list = Agent.objects.all()

    context = {
        'agents': agents_list,
    }
    return render(request, 'agents.html', context)


def agent_detail(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    agent_properties = Property.objects.filter(agent=agent, status='available')

    context = {
        'agent': agent,
        'agent_properties': agent_properties,
    }
    return render(request, 'agent_detail.html', context)
