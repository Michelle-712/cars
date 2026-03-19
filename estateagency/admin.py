from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Agent, Property, PropertyImage, ContactMessage


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone', 'joined_at']
    search_fields = ['first_name', 'last_name', 'email']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'city', 'property_type', 'listing_type', 'status', 'price', 'is_featured', 'created_at']
    list_filter = ['property_type', 'listing_type', 'status', 'is_featured', 'city']
    search_fields = ['title', 'address', 'city']
    list_editable = ['status', 'is_featured']


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'caption']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'subject', 'property', 'sent_at']
    search_fields = ['name', 'email', 'subject']
    readonly_fields = ['sent_at']