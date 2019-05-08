from django.shortcuts import render
from app.forms import *
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
        print("gh")
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