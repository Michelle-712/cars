"""
URL configuration for city project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from estateagency import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── Public Pages ──────────────────────────────────────────────
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('properties/', views.properties, name='properties'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('agents/', views.agents_list, name='agents'),
    path('agents/<int:pk>/', views.agent_detail, name='agent_detail'),

    # ── Authentication ────────────────────────────────────────────
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # ── Dashboard ─────────────────────────────────────────────────
    path('dashboard/', views.dashboard, name='dashboard'),

    # ── Property CRUD ─────────────────────────────────────────────
    path('dashboard/properties/', views.dashboard_properties, name='dashboard_properties'),
    path('dashboard/properties/add/', views.property_create, name='property_create'),
    path('dashboard/properties/<int:pk>/edit/', views.property_update, name='property_update'),
    path('dashboard/properties/<int:pk>/delete/', views.property_delete, name='property_delete'),

    # ── Agent CRUD ────────────────────────────────────────────────
    path('dashboard/agents/', views.dashboard_agents, name='dashboard_agents'),
    path('dashboard/agents/add/', views.agent_create, name='agent_create'),
    path('dashboard/agents/<int:pk>/edit/', views.agent_update, name='agent_update'),
    path('dashboard/agents/<int:pk>/delete/', views.agent_delete, name='agent_delete'),

    # ── Messages ──────────────────────────────────────────────────
    path('dashboard/messages/', views.dashboard_messages, name='dashboard_messages'),
    path('dashboard/messages/<int:pk>/delete/', views.message_delete, name='message_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)