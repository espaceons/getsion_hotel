from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class TypeChambre(models.Model):
    """Types de chambres (Standard, Deluxe, Suite...)"""
    nom = models.CharField(max_length=50)
    description = models.TextField()
    prix_nuit = models.DecimalField(max_digits=8, decimal_places=2)
    capacite = models.PositiveIntegerField()
    
    def __str__(self):
        return self.nom

class Chambre(models.Model):
    """Chambre physique dans l'hôtel"""
    numero = models.CharField(max_length=10, unique=True)
    etage = models.PositiveIntegerField()
    type_chambre = models.ForeignKey(TypeChambre, on_delete=models.PROTECT)
    statut_choices = [
        ('DISPONIBLE', 'Disponible'),
        ('OCCUPEE', 'Occupée'),
        ('NETTOYAGE', 'En nettoyage'),
        ('MAINTENANCE', 'En maintenance'),
    ]
    statut = models.CharField(max_length=12, choices=statut_choices, default='DISPONIBLE')
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Chambre {self.numero} ({self.type_chambre.nom})"

class Equipement(models.Model):
    """Équipements disponibles dans les chambres"""
    nom = models.CharField(max_length=100)
    icone = models.CharField(max_length=50)  # Pour Font Awesome

    def __str__(self):
        return self.nom

class ChambreEquipement(models.Model):
    """Relation many-to-many entre chambres et équipements"""
    chambre = models.ForeignKey(Chambre, on_delete=models.CASCADE)
    equipement = models.ForeignKey(Equipement, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)
    
    etat_choices = [
        ('BON', 'Bon état'),
        ('MOYEN', 'État moyen'), 
        ('MAINTENANCE', 'En maintenance'),
        ('A_REMPLACER', 'À remplacer'),
    ]
    
    etat = models.CharField(
        max_length=12, 
        choices=etat_choices, 
        default='BON'
    )

    class Meta:
        unique_together = ('chambre', 'equipement')
        verbose_name = "Équipement de chambre"
        verbose_name_plural = "Équipements de chambre"

    def __str__(self):
        return f"{self.equipement.nom} (Chambre {self.chambre.numero})"