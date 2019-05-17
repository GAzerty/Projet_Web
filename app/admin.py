from django.contrib import admin
from app.models import Joueur, Quartier, Amis, Rencontre, Stade, Inviter, Participer


class JoueurAdmin(admin.ModelAdmin):
    list_display = ('idJoueur','quartierJoueur',) #On renseigne les attributs qui seront affichés sur la page admin
    search_fields = ('quartierJoueur',)  #Les attributs utilisés pour la recherche

class QuartierAdmin(admin.ModelAdmin):
    list_display = ('idQuartier','nomQuartier')
    search_fields = ('idQuartier','nomQuartier')

class AmisAdmin(admin.ModelAdmin):
    list_display = ('joueur1Amis','joueur2Amis','etatJoueur1','etatJoueur2')
    search_fields = ('joueur1Amis','joueur2Amis')

class RencontreAdmin(admin.ModelAdmin):
    list_display = ('idRencontre','lieuRencontre','dateRencontre')
    search_fields = ('idRencontre','lieuRencontre','dateRencontre')

class StadeAdmin(admin.ModelAdmin):
    list_display = ('idStade','nomStade','villeStade')
    search_fields = ('idStade','nomStade','villeStade')

class InviterAdmin(admin.ModelAdmin):
    list_display = ('idJoueur','idRencontre','joueurDemandeur')
    search_fields = ('idJoueur','idRencontre','joueurDemandeur')

class ParticiperAdmin(admin.ModelAdmin):
    list_display = ('idJoueur','idRencontre','nombreButs','equipe')
    search_fields = ('idJoueur','idRencontre','equipe')



#On enregistre chaque modèle avec la configuration que l'on a établie au-dessus.
admin.site.register(Joueur,JoueurAdmin)
admin.site.register(Quartier,QuartierAdmin)
admin.site.register(Amis,AmisAdmin)
admin.site.register(Rencontre,RencontreAdmin)
admin.site.register(Stade,StadeAdmin)
admin.site.register(Inviter,InviterAdmin)
admin.site.register(Participer,ParticiperAdmin)

#L'administrateur du site peut maintenant réaliser toutes les actions de bases (CRUD) sur les modèles.