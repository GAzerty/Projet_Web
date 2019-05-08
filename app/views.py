from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from app.forms import SignupJoueurForm
from django.contrib.auth.models import User
from app.models import Joueur




# ---- VIEWS BASIQUES

def accueil(request):
    return render(request, 'index.html')

#def login()

#def loggout()

#change psswd()

#delete account()



# ---- VIEWS JOUEUR

#CREATE
def signupJoueur(request):
    if request.method == "POST":
        form = SignupJoueurForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data('username')
            raw_password = form.cleaned_data('password1')
            user = authenticate(username=username,password=raw_password)
            Utilisateur = User.objects.get(username=username)
            new_Joueur = Joueur(idJoueur=Utilisateur,idQuartier=form.cleaned_data('choix_quartier'))
            new_Joueur.save()
            login(request,user)
            return redirect('accueil')
    else:
        form = SignupJoueurForm()
        return render(request, "signup_joueur.html", {'SignupJoueurForm': form})


#READ


#UPDATE


#DELETE







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