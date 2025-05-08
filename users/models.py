from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('staff', 'Employé'),
        ('admin', 'Administrateur'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='staff')
    department = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class StaffProfile(models.Model):
    """Profil professionnel automatique pour staff/admin"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='staff_profile'
    )
    phone = models.CharField(max_length=20)
    hire_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"Profil professionnel de {self.user.username}"

@receiver(post_save, sender=CustomUser)
def create_staff_profile(sender, instance, created, **kwargs):
    """Crée automatiquement un profil staff lors de la création d'un utilisateur"""
    if created:
        StaffProfile.objects.create(user=instance)