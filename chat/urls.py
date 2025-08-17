"""
URL patterns for the chat application.
"""
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    # Dashboard and main views
    path('', views.dashboard, name='dashboard'),
    
    # Message management
    path('send/', views.send_message, name='send_message'),
    path('messages/', views.view_messages, name='view_messages'),
    path('messages/<int:message_id>/decrypt/', views.decrypt_message, name='decrypt_message'),
    
    # Key management
    path('keys/', views.manage_keys, name='manage_keys'),
    path('keys/generate/', views.generate_keys, name='generate_keys'),
    path('keys/import/', views.import_key, name='import_key'),
    path('keys/export/', views.export_public_key, name='export_public_key'),
    path('keys/<int:key_id>/details/', views.get_key_details, name='get_key_details'),
    
    # Key exchange
    path('exchange/', views.key_exchange, name='key_exchange'),
    
    # Security and logs
    path('security/', views.security_logs, name='security_logs'),
    path('security/overview/', views.security_overview, name='security_overview'),
]

