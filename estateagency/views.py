from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Property, Agent, ContactMessage
from .forms import PropertyForm, AgentForm, ContactForm, RegisterForm, LoginForm


# ─── Public Views ─────────────────────────────────────────────────────────────

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
    return render(request, 'about.html', {'agents': agents})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Your message has been sent! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'contact.html', {'form': form})


def properties(request):
    properties_list = Property.objects.filter(status='available')
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

    return render(request, 'properties.html', {'properties': properties_list})


def property_detail(request, pk):
    property = get_object_or_404(Property, pk=pk)
    related_properties = Property.objects.filter(city=property.city, status='available').exclude(pk=pk)[:3]
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save(commit=False)
            contact_msg.property = property
            contact_msg.subject = f'Enquiry about: {property.title}'
            contact_msg.save()
            messages.success(request, 'Your enquiry has been sent! An agent will contact you shortly.')
            return redirect('property_detail', pk=pk)

    return render(request, 'property_detail.html', {
        'property': property,
        'related_properties': related_properties,
        'form': form,
    })


def agents_list(request):
    agents = Agent.objects.all()
    return render(request, 'agents.html', {'agents': agents})


def agent_detail(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    agent_properties = Property.objects.filter(agent=agent, status='available')
    return render(request, 'agent_detail.html', {'agent': agent, 'agent_properties': agent_properties})


# ─── Authentication Views ─────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f'Welcome, {user.first_name}! Your account has been created.')
        return redirect('dashboard')
    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f'Welcome back, {user.first_name or user.username}!')
        return redirect(request.GET.get('next', 'dashboard'))
    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ─── Dashboard ────────────────────────────────────────────────────────────────

@login_required
def dashboard(request):
    total_properties = Property.objects.count()
    available_properties = Property.objects.filter(status='available').count()
    sold_properties = Property.objects.filter(status='sold').count()
    rented_properties = Property.objects.filter(status='rented').count()
    total_agents = Agent.objects.count()
    total_messages = ContactMessage.objects.count()
    recent_properties = Property.objects.order_by('-created_at')[:5]
    recent_messages = ContactMessage.objects.order_by('-sent_at')[:5]

    return render(request, 'dashboard/dashboard.html', {
        'total_properties': total_properties,
        'available_properties': available_properties,
        'sold_properties': sold_properties,
        'rented_properties': rented_properties,
        'total_agents': total_agents,
        'total_messages': total_messages,
        'recent_properties': recent_properties,
        'recent_messages': recent_messages,
    })


# ─── Property CRUD ────────────────────────────────────────────────────────────

@login_required
def property_create(request):
    form = PropertyForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Property added successfully!')
        return redirect('dashboard_properties')
    return render(request, 'dashboard/property_form.html', {'form': form, 'action': 'Add'})


@login_required
def dashboard_properties(request):
    properties_list = Property.objects.all().order_by('-created_at')
    return render(request, 'dashboard/properties_list.html', {'properties': properties_list})


@login_required
def property_update(request, pk):
    property = get_object_or_404(Property, pk=pk)
    form = PropertyForm(request.POST or None, request.FILES or None, instance=property)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Property updated successfully!')
        return redirect('dashboard_properties')
    return render(request, 'dashboard/property_form.html', {'form': form, 'action': 'Update', 'property': property})


@login_required
def property_delete(request, pk):
    property = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Property deleted successfully!')
        return redirect('dashboard_properties')
    return render(request, 'dashboard/property_confirm_delete.html', {'property': property})


# ─── Agent CRUD ───────────────────────────────────────────────────────────────

@login_required
def dashboard_agents(request):
    agents_list = Agent.objects.all()
    return render(request, 'dashboard/agents_list.html', {'agents': agents_list})


@login_required
def agent_create(request):
    form = AgentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Agent added successfully!')
        return redirect('dashboard_agents')
    return render(request, 'dashboard/agent_form.html', {'form': form, 'action': 'Add'})


@login_required
def agent_update(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    form = AgentForm(request.POST or None, request.FILES or None, instance=agent)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Agent updated successfully!')
        return redirect('dashboard_agents')
    return render(request, 'dashboard/agent_form.html', {'form': form, 'action': 'Update', 'agent': agent})


@login_required
def agent_delete(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.delete()
        messages.success(request, 'Agent deleted successfully!')
        return redirect('dashboard_agents')
    return render(request, 'dashboard/agent_confirm_delete.html', {'agent': agent})


# ─── Messages Dashboard ───────────────────────────────────────────────────────

@login_required
def dashboard_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-sent_at')
    return render(request, 'dashboard/messages_list.html', {'messages': messages_list})


@login_required
def message_delete(request, pk):
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted.')
        return redirect('dashboard_messages')
    return render(request, 'dashboard/message_confirm_delete.html', {'message': message})