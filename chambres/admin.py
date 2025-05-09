from django.contrib import admin
from .models import TypeChambre, Chambre, Equipement, ChambreEquipement

# admin.py
class ChambreEquipementInline(admin.TabularInline):
    model = ChambreEquipement
    extra = 1
    fields = ('equipement', 'quantite', 'etat')  # Ajout du champ etat
    readonly_fields = ('get_etat_color',)
    
    def get_etat_color(self, obj):
        colors = {
            'BON': 'green',
            'MOYEN': 'orange',
            'MAINTENANCE': 'red',
            'A_REMPLACER': 'darkred'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.etat, 'black'),
            obj.get_etat_display()
        )
    get_etat_color.short_description = "État (couleur)"

@admin.register(ChambreEquipement)
class ChambreEquipementAdmin(admin.ModelAdmin):
    list_display = ('chambre', 'equipement', 'quantite', 'get_etat_display_colored')
    list_filter = ('etat', 'equipement')
    
    def get_etat_display_colored(self, obj):
        colors = {
            'BON': 'success',
            'MOYEN': 'warning',
            'MAINTENANCE': 'danger',
            'A_REMPLACER': 'dark'
        }
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            colors.get(obj.etat, 'secondary'),
            obj.get_etat_display()
        )
    get_etat_display_colored.short_description = "État"