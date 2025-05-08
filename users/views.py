from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from dashboard.views import dashboard_redirect
from .forms import CustomUserCreationForm, CustomLoginForm
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters


# Vue d'inscription (réservée aux admins)
@login_required
def register_view(request):
    # Seuls les admins peuvent créer des comptes
    if not request.user.role == 'admin':
        messages.error(request, "Accès réservé aux administrateurs")
        return redirect('dashboard:dashboard_redirect')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Message de succès
            messages.success(
                request, 
                f"Compte créé pour {user.username} ({user.get_role_display()})"
            )
            return redirect('user_management')  # Rediriger vers la gestion des utilisateurs
            
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form': form,
        'title': 'Création de compte staff'
    }
    return render(request, 'users/register.html', context)

@sensitive_post_parameters()  # Protège les données sensibles (mot de passe)
@never_cache  # Empêche la mise en cache de la page de login
def login_view(request):
    """
    Vue de connexion sécurisée pour les utilisateurs staff/admin
    """
    # Redirection si déjà authentifié
    if request.user.is_authenticated:
        redirect_url = get_redirect_url(request.user)
        return redirect(redirect_url)

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            
            # Vérification du rôle avant connexion
            if not hasattr(user, 'role') or user.role not in ['admin', 'staff']:
                messages.error(
                    request,
                    "Accès réservé au personnel autorisé. Contactez l'administrateur."
                )
                return redirect('login')
            
            # Vérification de l'état actif du compte
            if not user.is_active:
                messages.error(
                    request,
                    "Votre compte est désactivé. Contactez l'administrateur."
                )
                return redirect('login')
            
            # Connexion effective
            login(request, user)
            
            # Gestion de "Remember me" si présent dans le formulaire
            if not form.cleaned_data.get('remember_me', True):
                request.session.set_expiry(0)  # Session expire quand le navigateur se ferme
            
            # Redirection vers 'next' ou le dashboard par défaut
            next_url = request.POST.get('next', 'dashboard:redirect')
            return redirect(next_url)
            
            # Journalisation (à implémenter selon vos besoins)
            # logger.info(f"Connexion réussie pour {user.username}")
            
            messages.success(request, f"Bienvenue, {user.username}!")
            return redirect(get_redirect_url(user))
        
        # Gestion des erreurs de formulaire
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Erreur {field}: {error}")
    else:
        form = CustomLoginForm()

    context = {
        'form': form,
        'hide_navbar': True,  # Optionnel: masque la navbar sur la page de login
        'login_page': True    # Pour le CSS/JS spécifique
    }
    return render(request, 'users/login.html', context)

def get_redirect_url(user):
    """
    Détermine la page de redirection après connexion
    """
    if user.role == 'admin':
        return 'dashboard:admin_dashboard'
    return 'dashboard:staff_dashboard'

# Déconnexion sécurisée
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, "Vous avez été déconnecté avec succès")
    return redirect('users:login')

# Fonction utilitaire pour les redirections
def get_redirect_url(user):
    """Détermine la page de redirection après connexion"""
    if user.role == 'admin':
        return 'admin_dashboard'
    return 'staff_dashboard'

# Vue tableau de bord protégée
@login_required
def dashboard_redirect(request):
    """Redirige vers le bon dashboard selon le rôle"""
    return redirect(get_redirect_url(request.user))