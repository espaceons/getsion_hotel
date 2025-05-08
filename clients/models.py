from django.db import models
from django.contrib.auth import get_user_model
import uuid

# Récupère dynamiquement le modèle utilisateur personnalisé
User = get_user_model()

class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qr_token = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)

    def __str__(self):
        return f"Client Profile of {self.user.username}"
