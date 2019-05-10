from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
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
    liste_amis = Amis.objects.filter(Q(joueur1Amis=joueur) | Q(joueur2Amis=joueur))  # Liste d'Amis du joueur
    amis_valide = []
    print(liste_amis)
    for ami in liste_amis:
        if ami.amitie_valide(): #On vérifie que la liaison est valide (réciproque)
            amis_valide.append(ami)
    print(amis_valide)
    return amis_valide

#Retourne les demandes reçus et en attente du joueur en paramètre
def mesDemandes(joueur):
    liste_amis = Amis.objects.filter(joueur2Amis=joueur)  # Liste d'Amis du joueur
    demande_amis = []
    for ami in liste_amis:
        if not ami.amitie_valide(): #Si le test renvoie False, cela signifie que la demande est encore en attente
            demande_amis.append(ami)
    return demande_amis

#View qui affiche une dashboard qui permet plusieurs fonctionnalités (demandeAmis,rechercheAmis,validerDemande,rejeterDemande)
def dashboardAmis(request):
    joueur = getJoueurConnecte(request)
    listeAmis = mesAmis(joueur)
    listeDemandes = mesDemandes(joueur)
    return render(request, "amis/dashboard_amis.html",locals())

#View qui recherche un ami, à partir d'un username
#Réalisé via AJAX
def rechercheAmis(request):
    usernameAmis = request.POST.get('recherche_usernameAmis')  #Récupération de l'username
    utilisateur = User.objects.filter(username=usernameAmis)
    if not utilisateur:# Si on ne trouve pas l'utilisateur en question
        existe = False
        feedback = "Aucun joueur ne correspond à ce nom"
    else:
        #joueur = Joueur.objects.get(idJoueur=utilisateur)
        existe = True
        feedback = "Joueur trouvé !"

    reponse = {
        'existe':existe,
        'feedback':feedback,
        'username':usernameAmis,
    }
    return JsonResponse(reponse)

#CREATE
#Creation de Amis, prend en paramètre le username de l'amis à qui l'on envoie la demande
#Réalisé via AJAX
def demandeAmis(request):
    usernameAmis = request.POST.get('demande_usernameAmis') #Récupération de l'username

    utilisateur_recipient =  User.objects.filter(username=usernameAmis)#NB: Un unsername est unique pour chaque User
    if not utilisateur_recipient:
        succes=False
        feedback = "Aucun joueur ne correspond à ce nom."
    else:
        joueur_sender = getJoueurConnecte(request)#C'est le joueur qui réalise la demande en Amis
        joueur_recipient = Joueur.objects.get(idJoueur=utilisateur_recipient[0])

        #Testons si une amitié existe déjà entre ces deux joueurs:
        intergrity_amis = Amis.objects.filter(Q(Q(joueur1Amis=joueur_sender) & Q(joueur2Amis=joueur_recipient)) | Q(Q(joueur1Amis=joueur_recipient) & Q(joueur2Amis=joueur_sender)))

        if joueur_recipient.idJoueur==joueur_sender.idJoueur: #Un joueur ne peut pas s'ajouter en ami lui-même
            succes=False
            feedback = "Vous ne pouvez pas vous ajouter en ami."
        elif not intergrity_amis: #Si aucune relation n'a été trouvée
            demande_amis = Amis(joueur1Amis=joueur_sender,joueur2Amis=joueur_recipient)#etatJoueur1 et etatJoueur2 possède des valeurs par défaut, donc nous n'avons pas besoin de les mentionner ici
            demande_amis.save()
            succes=True
            feedback = "Votre demande à été envoyée avec succès."
        else:
            succes=False
            feedback = "Une demande d'ami existe déjà avec "+usernameAmis+"."

    reponse = {
        "succes":succes,
        "feedback":feedback,
    }
    return JsonResponse(reponse)


#UPDATE
#Accepte la demande en amis
#Le joueur accepte la demande qui lui a été envoyée
#Réalisé via AJAX
def accepteAmis(request):
    username_sender = request.POST.get('username_sender')
    utilisateur_sender = User.objects.filter(username=username_sender)
    if not utilisateur_sender:        #Le username_sender n'appartient à aucun utilisateur, possible tentative d'usurpation
        succes = False
        feedback = "Aucun utilisateur ne correspond"
    else:
        joueur_sender = Joueur.objects.get(idJoueur=utilisateur_sender[0])
        joueur_recipient = getJoueurConnecte(request)
        relation_amis = Amis.objects.filter(joueur1Amis=joueur_sender, joueur2Amis=joueur_recipient)
        if not relation_amis:
            succes = False
            feedback = "Aucune demande d'ami existante"
        else:
            if relation_amis[0].amitie_valide():
                succes = False
                feedback = "Vous avez déjà accepté "+username_sender+" en ami !"
            else:
                relation_amis[0].etatJoueur2 = "AC"
                relation_amis[0].save()
                succes = True
                feedback = "Vous avez accepté " + username_sender + " en ami !"

    reponse = {
        'succes' : succes,
        'feedback' : feedback,
    }
    return JsonResponse(reponse)

#DELETE
#Refuser une demande & Annuler une demande
#Supprime la liaison entre deux joueur.
def supprimerAmis(request):
    username= request.POST.get('username')
    utilisateur = User.objects.filter(username=username)
    if not utilisateur:        #Le username_sender n'appartient à aucun utilisateur, possible tentative d'usurpation
        succes = False
        feedback = "Aucun utilisateur ne correspond."
    else:
        joueur1 = Joueur.objects.get(idJoueur=utilisateur[0])
        joueur2 = getJoueurConnecte(request)
        relation_amis = Amis.objects.filter(Q(Q(joueur1Amis=joueur1) & Q(joueur2Amis=joueur2)) | Q(Q(joueur1Amis=joueur2) & Q(joueur2Amis=joueur2))) # Un seul résultat possible a cette requête
        if not relation_amis:
            succes = False
            feedback = "Aucune amitié existante."
        else:
            relation_amis[0].delete()
            succes = False
            feedback = "Amitié supprimé."

    reponse = {
        'succes' : succes,
        'feedback' : feedback,
    }
    return JsonResponse(reponse)

#READ
#List







# ---- VIEWS RENCONTRE

#CREATE

#READ

#UPDATE

#DELETE


# ---- VIEWS PARTICIPER

#CREATE

#READ

#UPDATE

#DELETE











# --- POUR L'ADMIN

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