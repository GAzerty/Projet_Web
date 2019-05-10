from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from app.forms import SignupJoueurForm, UpdateJoueurForm
from django.contrib.auth.models import User
from app.models import Joueur, Quartier, Amis
from django.http import JsonResponse



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
    utilisateur = User.objects.get(username=request.user.username).delete()
    return render(request, "index.html")







# ---- VIEWS AMIS

#Retourne les amitié réciproque du joueur passé en paramètre
def mesAmis(joueur):
    liste_amis = Amis.objects.filter(joueur1Amis=joueur)  # Liste d'Amis du joueur connecté, avec potentiellement
    amis_valide = []
    for ami in liste_amis:
        if ami.amitie_valide(): #On vérifie que la liaison est valide (réciproque)
            amis_valide.append(ami)
    return amis_valide

#Retourne les demandes reçus et en attente du joueur en paramètre
def mesDemandes(joueur):
    liste_amis = Amis.objects.filter(joueur2Amis=joueur)  # Liste d'Amis du joueur connecté, avec potentiellement
    demande_amis = []
    for ami in liste_amis:
        if not ami.amitie_valide(): #Si le test renvoie False, cela signifie que la demande est encore en attente
            demande_amis.append(ami)
    return demande_amis

def dashboardAmis(request):
    joueur = getJoueurConnecte(request)
    listeAmis = mesAmis(joueur)
    listeDemandes = mesDemandes(joueur)
    return render(request, "amis/dashboard_amis.html",locals())

#CREATE
#Creation de Amis, prend en paramètre le username de l'amis à qui l'on envoie la demande
#Réalisé via AJAX
def demandeAmis(request):
    usernameAmis = request.POST.get('demande_usernameAmis') #Récupération de l'username

    utilisateur_recipient = get_object_or_404(User, username=usernameAmis)#NB: Un unsername est unique pour chaque User
    joueur_sender = getJoueurConnecte(request)#C'est le joueur qui réalise la demande en Amis
    joueur_recipient = get_object_or_404(Joueur, idJoueur=utilisateur_recipient)

    #Testons si une amitié existe déjà entre ces deux joueurs:
    intergrity_amis = Amis.objects.get(joueur1Amis=joueur_sender,joueur2Amis=joueur_recipient)
    if not intergrity_amis: #Si aucune relation n'a été trouvée
        demande_amis = Amis(joueur1Amis=joueur_sender,joueur2Amis=joueur_recipient)#etatJoueur1 et etatJoueur2 possède des valeurs par défaut, donc nous n'avons pas besoin de les mentionner ici
        demande_amis.save()
        feedback = "Votre demande à été envoyée avec succès."
    else:
        feedback = "Vous avez déjà envoyé une demande à "+usernameAmis+". Attendez sa réponse !"

    reponse = {
        "feedback":feedback,
    }
    return JsonResponse(reponse)

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