from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Quartier, Rencontre, Stade, Participer






# ----- FORMULAIRES DU MODÈLE JOUEUR ---------- :

#Création du champ QuartierChoiceField à partir de ModelChoiceField
#Cela nous permettra d'avoir un élément HTML Select dans notre formulaire avec l'ensemble des Quartiers comme choix
class QuartierChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nomQuartier

#Formulaire de creation de Joueur
#Création du formulaire à partir de UserCreationForm, le formulaire utilisé de base par Django pour la création d'utilisateur
class SignupJoueurForm(UserCreationForm):
    choix_quartier = QuartierChoiceField(queryset=Quartier.objects.all(), to_field_name='idQuartier', label="Quartier") #Champ de formulaire pour que l'utilisateur choisisse son quartier
    email = forms.EmailField(required=True) #L'email de l'utilisateur est requis en prévision d'un changement de mot de passe et autre situations

    class Meta(UserCreationForm.Meta):
        model = User                    #Le model associé à notre formulaire est le modèle User de Django
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','email','choix_quartier',) #Les fields de UserCreationForm sont username, password1, password2, on rajoute les fields de User et choix_quartier.

#Formulaire de mise à jour de Joueur
class UpdateJoueurForm(forms.Form):
    first_name = forms.CharField(label = "Prénom", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label = "Nom",  widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Adresse éléctonique", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    choix_quartier = QuartierChoiceField(queryset=Quartier.objects.all(), to_field_name='idQuartier', label="Quartier", widget=forms.Select(attrs={'class': 'form-control'})) #Champ de formulaire pour que l'utilisateur choisse sont quartier


#----- FORMULAIRES RENCONTRE ------- :


#Création du champ StadeChoiceField à partir de ModelChoiceField
class StadeChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.nomStade

#Formulaire de Creation et de Mise à jour de Rencontre
#Formulaire créé à partir du modèle Rencontre
class CreationRencontreForm(ModelForm):
    choix_stade = StadeChoiceField(queryset=Stade.objects.all(), to_field_name="idStade", label="Stade",widget=forms.Select(attrs={'class': 'form-control'}))
    heureMatch = forms.TimeField(label="Heure de la rencontre",help_text="Format 'H':'M'")
    class Meta:
        model = Rencontre           #Modèle associé
        fields = ['dateRencontre',]
        labels = {
            'dateRencontre':'Date de la rencontre',
        }
        widgets = {
            'dateRencontre': forms.SelectDateWidget(years=range(2019, 2020)), #L'année disponible pour fixer la date de la rencontre
        }


#----- FORMULAIRES PARTICIPER
class UpdateParticiperForm(ModelForm):
    class Meta:
        model = Participer                 #Le modèle associé que l'on associe au formulaire
        fields = ['nombreButs','equipe'] #Les champs accessible dans le formulaire

