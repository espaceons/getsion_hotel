from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.html import format_html
from .models import Chambre, TypeChambre

#@login_required
#def liste_chambres(request):
 #   """
#    Liste complète des chambres avec filtres avancés
#    """
    # Récupération des paramètres de filtrage
#    etage = request.GET.get('etage')
#    type_chambre = request.GET.get('type')
#    statut = request.GET.get('statut')

    # Construction de la requête de base
#    chambres = Chambre.objects.select_related('type_chambre').order_by('numero')

    # Application des filtres
#    if etage:
#        chambres = chambres.filter(etage=etage)
#    if type_chambre:
#        chambres = chambres.filter(type_chambre__id=type_chambre)
#    if statut:
#        chambres = chambres.filter(statut=statut)
#
#    context = {
#        'chambres': chambres,
#        'types_chambre': TypeChambre.objects.all(),
#        'statuts_choices': dict(Chambre.statut_choices),
#        'current_filters': {
#            'etage': etage,
#            'type': type_chambre,
#            'statut': statut
#        }
#    }
#    return render(request, 'chambres/liste.html', context)

#@login_required
#def chambres_disponibles(request):
 #   """
 #   Liste des chambres disponibles avec capacité de filtrage
#    """
#    # Récupération des paramètres optionnels
#    capacite_min = request.GET.get('capacite_min', 1)
#    date_arrivee = request.GET.get('date_arrivee')  # À intégrer avec le module réservation
#
#    chambres = Chambre.objects.filter(
#        statut='DISPONIBLE'
#    ).select_related('type_chambre').order_by('numero')
#
#    # Filtre supplémentaire par capacité
#    chambres = chambres.filter(
#        type_chambre__capacite__gte=capacite_min
#    )
#
#    context = {
#        'chambres': chambres,
#        'capacite_min': capacite_min,
#        'date_arrivee': date_arrivee
#    }
#    return render(request, 'chambres/disponibles.html', context)

#@login_required
#def detail_chambre(request, pk):
#    """
#    Détail complet d'une chambre avec ses équipements
#    """
#    chambre = get_object_or_404(
#        Chambre.objects.prefetch_related(
#            'chambreequipement_set__equipement'
#        ), 
#        pk=pk
#    )

    # Préparation des données pour le template
#    equipements = []
#    for ce in chambre.chambreequipement_set.all():
#        equipements.append({
#            'nom': ce.equipement.nom,
#            'quantite': ce.quantite,
#            'etat': ce.get_etat_display(),
#            'etat_class': get_etat_class(ce.etat),  # Appel direct sans self
#            'icone': getattr(ce.equipement, 'icone', 'fa-cube')
#        })

#    context = {
#        'chambre': chambre,
#        'equipements': equipements,
#        'statut_class': get_statut_class(chambre.statut)  # Appel direct sans self
#    }
#    return render(request, 'chambres/detail.html', context)

# Méthodes utilitaires
#def get_etat_class(self, etat):
#    """Retourne la classe CSS selon l'état de l'équipement"""
#    return {
#        'BON': 'text-success',
#        'MOYEN': 'text-warning',
#        'MAINTENANCE': 'text-danger',
#        'A_REMPLACER': 'text-dark'
#    }.get(etat, 'text-secondary')

#def get_statut_class(self, statut):
#    """Retourne la classe CSS selon le statut de la chambre"""
#    return {
#        'DISPONIBLE': 'bg-success',
#        'OCCUPEE': 'bg-danger',
#        'NETTOYAGE': 'bg-warning',
#        'MAINTENANCE': 'bg-dark'
#    }.get(statut, 'bg-secondary')


from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Chambre, TypeChambre
from .forms import ChambreForm

class ChambreListView(ListView):
    model = Chambre
    template_name = 'chambres/chambre_liste.html'
    context_object_name = 'chambres'
    paginate_by = 10

class ChambreCreateView(CreateView):
    model = Chambre
    form_class = ChambreForm
    template_name = 'chambres/chambre_form.html'
    success_url = reverse_lazy('chambres:chambre_liste')

class ChambreUpdateView(UpdateView):
    model = Chambre
    form_class = ChambreForm
    template_name = 'chambres/chambre_form.html'
    success_url = reverse_lazy('chambres:chambre_liste')

class ChambreDeleteView(DeleteView):
    model = Chambre
    template_name = 'chambres/chambre_confirm_delete.html'
    success_url = reverse_lazy('chambres:chambre_liste')

class ChambreDetailView(DetailView):
    model = Chambre
    template_name = 'chambres/chambre_detail.html'
