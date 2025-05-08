from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordResetForm



class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role']

class StaffCreationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'department']
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            # Met à jour le profil avec le téléphone
            user.staff_profile.phone = self.cleaned_data['phone']
            user.staff_profile.save()
        return user

class StaffLoginForm(AuthenticationForm):
    pass


class CustomLoginForm(AuthenticationForm):
    # Ajout de champs supplémentaires si besoin
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des champs
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })

    def confirm_login_allowed(self, user):
        """Vérifie que l'utilisateur peut se connecter"""
        super().confirm_login_allowed(user)
        
        # Vérification supplémentaire pour staff/admin seulement
        if user.role not in ['admin', 'staff']:
            raise ValidationError(
                "Ce compte n'a pas les droits d'accès au système.",
                code='invalid_role'
            )
        
        # Vous pouvez ajouter d'autres vérifications ici
        # Par exemple, vérifier si le compte est actif
        if not user.is_active:
            raise ValidationError(
                "Ce compte est désactivé.",
                code='inactive_account'
            )
