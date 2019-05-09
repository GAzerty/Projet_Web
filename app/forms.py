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
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','email','choix_quartier',) #Les fields de UserCreationForm sont username, password1, password2, etc..

#Formulaire de mise à jour de Joueur
class UpdateJoueurForm(forms.Form):
    first_name = forms.CharField(label = "Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label = "Nom",  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Adresse éléctonique", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    choix_quartier = QuartierChoiceField(queryset=Quartier.objects.all(), to_field_name='idQuartier', label="Quartier", widget=forms.Select(attrs={'class': 'form-control'})) #Champ de formulaire pour que l'utilisateur choisse sont quartier
