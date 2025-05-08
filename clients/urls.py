from django.urls import path
from . import views

urlpatterns = [
    path('qr/<int:user_id>/', views.generate_qr, name='generate_qr'),  # Générer QR pour le client
    path('scan-login/<str:qr_token>/', views.scan_login, name='scan_login'),  # Login via QR code
]
