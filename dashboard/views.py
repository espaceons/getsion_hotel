from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

# Vue qui redirige vers le dashboard approprié
@login_required
def dashboard_redirect(request):
    user = request.user

    # Redirection vers le dashboard en fonction du rôle
    if user.role == 'admin':
        return redirect('dashboard:admin_dashboard')
    elif user.role == 'staff':
        return redirect('dashboard:staff_dashboard')
    elif user.role == 'client':
        return redirect('dashboard:client_dashboard')
    else:
        # Si un utilisateur avec un rôle non défini essaie de se connecter
        return redirect('login')
    


# Dashboard pour les administrateurs
@login_required
def admin_dashboard(request):
    return render(request, 'dashboard/dashboard_admin.html', {'user': request.user})

# Dashboard pour le staff
@login_required
def staff_dashboard(request):
    return render(request, 'dashboard/dashboard_staff.html', {'user': request.user})

# Dashboard pour les clients
@login_required
def client_dashboard(request):
    return render(request, 'dashboard/dashboard_client.html', {'user': request.user})

