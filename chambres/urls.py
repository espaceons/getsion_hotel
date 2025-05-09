from django.urls import path
#from . import views
from .views import (
    ChambreListView, 
    ChambreCreateView,
    ChambreUpdateView,
    ChambreDeleteView,
    ChambreDetailView
)

app_name = 'chambres'

urlpatterns = [
    #path('', views.liste_chambres, name='liste'),
    #path('disponibles/', views.chambres_disponibles, name='disponibles'),
    #path('<int:pk>/', views.detail_chambre, name='detail'),
    #path('types/', views.liste_types, name='types'),
    
    path('', ChambreListView.as_view(), name='chambre_liste'),
    path('ajouter/', ChambreCreateView.as_view(), name='chambre_ajouter'),
    path('<int:pk>/', ChambreDetailView.as_view(), name='chambre_detail'),
    path('<int:pk>/modifier/', ChambreUpdateView.as_view(), name='chambre_modifier'),
    path('<int:pk>/supprimer/', ChambreDeleteView.as_view(), name='chambre_supprimer'),
]