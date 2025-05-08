import qrcode
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from .models import ClientProfile
from django.contrib.auth.decorators import login_required


def generate_qr(request, user_id):
    client_profile = ClientProfile.objects.get(user_id=user_id)
    qr_data = f"http://yourdomain.com/scan-login/{client_profile.qr_token}/"
    
    # Générer un QR code
    img = qrcode.make(qr_data)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

def scan_login(request, qr_token):
    try:
        client_profile = ClientProfile.objects.get(qr_token=qr_token)
        user = authenticate(request, username=client_profile.user.username)
        if user:
            login(request, user)
            return redirect('client_dashboard')  # Page après login
        else:
            return HttpResponse("Erreur de connexion", status=400)
    except ClientProfile.DoesNotExist:
        return HttpResponse("Token QR invalide", status=400)


@login_required
def client_dashboard(request):
    return render(request, 'dashboard/dashboard.html', {'user': request.user})# le dashboard pour tous les utilisateurs avec condition .