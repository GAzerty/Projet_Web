from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Quartier






# ----- FORMULAIRES JOUEUR :

#FORM CREATION JOUEUR

class QuartierChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nomQuartier

#Formulaire de creation de Joueur
class SignupJoueurForm(UserCreationForm):
    choix_quartier = QuartierChoiceField(queryset=Quartier.objects.all(), to_field_name='idQuartier', label="Quartier") #Champ de formulaire pour que l'utilisateur choisse sont quartier
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('choix_quartier',) #Les fields de UserCreationForm sont username, password1, password2, etc..

