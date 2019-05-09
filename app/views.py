from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from app.forms import SignupJoueurForm, UpdateJoueurForm
from django.contrib.auth.models import User
from app.models import Joueur, Quartier




# ---- VIEWS BASIQUES

def accueil(request):
    return render(request, 'index.html')

def logoutJoueur(request):
    logout(request)
    return render(request, 'index.html')

#change psswd()

#delete account()



# ---- VIEWS JOUEUR

#CREATE
def signupJoueur(request):
    if request.method == "POST":
        form = SignupJoueurForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username,password=raw_password)
            Utilisateur = User.objects.get(username=username)
            quartier = Quartier.objects.get(nomQuartier=form.cleaned_data['choix_quartier'])
            new_Joueur = Joueur(idJoueur=Utilisateur,quartierJoueur=quartier)
            new_Joueur.save()
            login(request,user)
            return render(request, 'index.html')
        else:
            return render(request, "signup_joueur.html", {'SignupJoueurForm': form})
    else:
        form = SignupJoueurForm()
        return render(request, "signup_joueur.html", {'SignupJoueurForm': form})


#READ - MON COMPTE

#Retourne un Joueur à partir de l'utilisateur connecté
def getJoueurConnecte(request):
    utilisateur = User.objects.get(username=request.user.username)  # Je récupère l'utilisateur connecté
    joueur = Joueur.objects.get(idJoueur=utilisateur)  # Je récupère le joueur correspondant à l'utilisateur
    return joueur

#@login_required
def moncompteJoueur(request):
    joueur = getJoueurConnecte(request)
    return render(request, "joueur/account.html", {'Joueur': joueur}) #Je renvoie le joueur à la template


#UPDATE
def updateJoueur(request):
    utilisateur = User.objects.get(username=request.user.username)
    joueur = Joueur.objects.get(idJoueur=utilisateur)
    if request.method == "POST":
        form = UpdateJoueurForm(request.POST)
        if form.is_valid():
            utilisateur.first_name = form.cleaned_data['first_name']
            utilisateur.last_name = form.cleaned_data['last_name']
            utilisateur.email = form.cleaned_data['email']
            utilisateur.save() #Sauvegarde de l'utilisateur avec ses nouvelles valeurs
            quartier = Quartier.objects.get(nomQuartier=form.cleaned_data['choix_quartier'])
            joueur.quartierJoueur = quartier
            joueur.save() #Sauvegarde du joueur avec ses nouvelles valeurs
            return moncompteJoueur(request)
        else:
            return render(request, "joueur/update_joueur.html", {'UpdateJoueurForm': form,'Joueur': joueur})
    else:
        dataform = {
            'first_name': utilisateur.first_name,
            'last_name': utilisateur.last_name,
            'email': utilisateur.email,
            'choix_quartier': joueur.quartierJoueur,
        }
        form = UpdateJoueurForm(dataform) #On lies les données de dataform avec le formulaire, les champs se remplissent en fonctions du nom des champs correspondant au formulaire
        return render(request, "joueur/update_joueur.html", {'UpdateJoueurForm': form,'Joueur': joueur})

#DELETE
def deleteJoueur(request):
    getJoueurConnecte(request).delete()
    utilisateur = User.objects.get(username=request.user.username).delete
    return render(request, "index.html")







# ---- VIEWS AMIS

#CREATE

#READ

#UPDATE

#DELETE





# ---- VIEWS PARTICIPER

#CREATE

#READ

#UPDATE

#DELETE





# ---- VIEWS RENCONTRE

#CREATE

#READ

#UPDATE

#DELETE






# ---- VIEWS STADE

#CREATE

#READ

#UPDATE

#DELETE





# ---- VIEWS QUARTIER

#CREATE

#READ

#UPDATE

#DELETE