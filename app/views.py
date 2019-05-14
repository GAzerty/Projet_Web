from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from app.forms import SignupJoueurForm, UpdateJoueurForm, CreationRencontreForm, StadeForm, UpdateParticiperForm
from django.contrib.auth.models import User
from app.models import Joueur, Quartier, Amis, Rencontre, Stade, Inviter, Participer
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from datetime import date
import random

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
        form = SignupJoueurForm()
    return render(request, "signup_joueur.html", {'SignupJoueurForm': form})


#READ - MON COMPTE

#Retourne un Joueur à partir de l'utilisateur connecté
def getJoueurConnecte(request):
    joueur = Joueur.objects.get(idJoueur=request.user)  # Je récupère le joueur correspondant à l'utilisateur
    return joueur

#@login_required
def moncompteJoueur(request):
    joueur = getJoueurConnecte(request)
    nbDemande = len(mesDemandes(joueur))
    nbInvitations = len(Inviter.objects.filter(idJoueur=joueur))
    return render(request, "joueur/account.html", {'Joueur': joueur,"NbDemandes":nbDemande,"NbInvitations":nbInvitations,}) #Je renvoie le joueur à la template


#UPDATE
def updateJoueur(request):
    utilisateur = request.user
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
    return render(request, "index.html")




# ---- VIEWS AMIS

#Retourne les amitié réciproque du joueur passé en paramètre
def mesAmis(joueur):
    liste_amis = Amis.objects.filter(Q(joueur1Amis=joueur) | Q(joueur2Amis=joueur))  # Liste d'Amis du joueur
    amis_valide = []
    for ami in liste_amis:
        if ami.amitie_valide(): #On vérifie que la liaison est valide (réciproque)
            amis_valide.append(ami)
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
    listeJoueurAmis=[]
    for ami in listeAmis:
        listeJoueurAmis.append(ami.monAmi(joueur))
    listeDemandes = mesDemandes(joueur)
    return render(request, "amis/dashboard_amis.html",{"listeDemandes":listeDemandes,"listeAmis":listeJoueurAmis})

#View qui recherche un ami, à partir d'un username
#Réalisé via AJAX
def rechercheAmis(request):
    usernameAmis = request.POST.get('rechercheUsername')  #Récupération de l'username du joueur que l'on recherche
    utilisateur = User.objects.filter(username=usernameAmis) #Un username est unique pour chaque joueur
    if not utilisateur:# Si on ne trouve pas l'utilisateur en question
        existe = False
        feedback = "Aucun joueur ne correspond à ce nom"
    else:
        #joueur = Joueur.objects.get(idJoueur=utilisateur[0])
        existe = True
        feedback = "Joueur trouvé !"

    reponse = {
        'succes':existe,
        'feedback':feedback,
        'username':usernameAmis,
    }
    return JsonResponse(reponse)

#CREATE
#Creation de Amis, prend en paramètre le username de l'amis à qui l'on envoie la demande
#Réalisé via AJAX
def demandeAmis(request):
    usernameAmis = request.POST.get('demandeUsername') #Récupération de l'username

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
    idUser_sender = request.POST.get('User')
    utilisateur_sender = User.objects.filter(id=idUser_sender)
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
                feedback = "Vous avez déjà accepté "+utilisateur_sender[0].username+" en ami !"
            else:
                relation_amis[0].etatJoueur2 = "AC"
                relation_amis[0].save()
                succes = True
                feedback = "Vous avez accepté " + utilisateur_sender[0].username + " en ami !"

    reponse = {
        'succes' : succes,
        'feedback' : feedback,
    }
    return JsonResponse(reponse)

#DELETE
#Refuser une demande & Annuler une demande
#Supprime la liaison entre deux joueur.
def supprimerAmis(request):
    idUser= request.POST.get('User')
    utilisateur = User.objects.filter(id=idUser)
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
def createRencontre(request):
    title="Organiser un match"
    buttonText="Créer la rencontre"
    if request.method == "POST":
        form = CreationRencontreForm(request.POST)
        if form.is_valid():
            new_rencontre = form.save(commit=False) #Création d'une rencontre, commit=False empêche la sauvegarde du nouvel objet
            stade = get_object_or_404(Stade, nomStade=form.cleaned_data['choix_stade'])
            new_rencontre.lieuRencontre = stade
            new_rencontre.save()
            joueur = getJoueurConnecte(request)
            createParticiper(joueur,new_rencontre)  #Le joueur qui a créé la rencontre participe automatiquement à la rencontre
            return inviterAmis(request,new_rencontre.idRencontre)
    else:
        form = CreationRencontreForm()
    return render(request, "rencontre/formRencontre.html", {"RencontreForm":form,"title":title,"buttonText":buttonText})



#READ
def readRencontre(request,idRencontre):
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre)
    participantsLocaux = Participer.objects.filter(idRencontre=rencontre,equipe="LOC")
    participantsVisiteurs = Participer.objects.filter(idRencontre=rencontre, equipe="VIS")

    #Test: L'utilisateur qui read la rencontre doit participer à la rencontre.
    #On affichera les bouttons de modifications et de suppression uniquement si il participe.
    joueur = getJoueurConnecte(request)
    participe = True
    if not Participer.objects.filter(idJoueur=joueur,idRencontre=rencontre):
        participe=False

    listInvite = Inviter.objects.filter(idRencontre=rencontre)
    nbParticipant = len(participantsLocaux)+len(participantsVisiteurs) #Le nombre de participant. Si il y a 1 participant, le boutton de suppression s'affiche à l'utilisateur.
    heure_match = rencontre.toString_Heure()
    return render(request, "rencontre/readRencontre.html",{"Rencontre":rencontre,"JoueursLocaux":participantsLocaux,"JoueursVisiteurs":participantsVisiteurs,"JoueursInvite":listInvite,"NbJoueurs":nbParticipant,"Participe":participe,"HeureMatch":heure_match,})

#LIST
#Retourne la liste des rencontre auquel le joueur participe
def listRencontre(request):
    joueur = getJoueurConnecte(request)
    listParticiper = Participer.objects.filter(idJoueur=joueur)
    print(listParticiper)
    listRencontreJoueur = []
    for participation in listParticiper:
        listRencontreJoueur.append(participation.idRencontre)
    print(listRencontreJoueur)
    return render(request, "rencontre/liste_rencontre.html", {"ListRencontre":listRencontreJoueur,})


#UPDATE
def updateRencontre(request,idRencontre):
    title="Modifier un match"
    buttonText="Modifier la rencontre"
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre)
    if request.method == "POST":
        form = CreationRencontreForm(request.POST)
        if form.is_valid():
            stade = get_object_or_404(Stade, nomStade=form.cleaned_data['choix_stade']) #On vérifie que le stade existe bien sinon on génère une exception 404
            rencontre.lieuRencontre = stade
            rencontre.dateRencontre = form.cleaned_data['dateRencontre']
            rencontre.heureRencontre = form.cleaned_data['heureRencontre']
            rencontre.save()
            return render(request, "accueil.html")
    else:
        dataform = {
            "choix_stade":rencontre.lieuRencontre,
            "dateRencontre":rencontre.dateRencontre,
            "heureRencontre":rencontre.heureRencontre,
        }
        form = CreationRencontreForm(dataform)

    return render(request, "rencontre/formRencontre.html", {"RencontreForm":form,"title":title,"buttonText":buttonText})

#DELETE
#Suppression d'une rencontre
#Vérifications spéciales :
#       -- Uniquement si le nombre de participant == 1.
#       -- Uniquement si le joueur participe à la rencontre.
def deleteRencontre(request,idRencontre):
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre)
    joueur = getJoueurConnecte(request)

    #Si l'utilisateur ne participe pas à la rencontre alors on génère une exception 403
    participe = Participer.objects.filter(idJoueur=joueur,idRencontre=rencontre)
    if (not participe) or (len(participe)>1):
        raise PermissionDenied

    if request.method == "POST":
        rencontre.delete()
        return listRencontre(request)
    return render(request, "delete.html", {"ObjetDelete":rencontre})





# ---- VIEWS INVITER

#Retourne une page permettant d'inviter les amis du joueur connecté à la rencontre passé en paramètre
def inviterAmis(request,idRencontre):
    #Init des valeurs de retour
    succes=True
    feedback=""

    joueur = getJoueurConnecte(request)
    listAmis = mesAmis(joueur) #Récupère les amis du joueur connecté
    listJoueurAmis =[]
    print(listAmis)
    for ami in listAmis:
        listJoueurAmis.append(ami.monAmi(joueur)) #Je récupère les joueur ami avec le joueur passé en paramètre
    print(listJoueurAmis)
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre)
    participation = Participer.objects.filter(idJoueur=joueur, idRencontre=rencontre)
    if not participation:
        succes=False
        feedback="Vous ne participez pas à cette rencontre. Vous n'avez pas la possibilité d'ajouter vos amis."
    return render(request , "inviter/amis_inviter.html", {"listJoueurAmis":listJoueurAmis,"Rencontre":rencontre,"succes":succes,"feedback":feedback})


#CREATE
def createInviter(request):
    idUser= request.POST.get('User') #Récupération de l'id du joueur
    idRencontre = request.POST.get('idRencontre')  # Récupération de l'username

    utilisateur_recipient =  User.objects.filter(id=idUser)#NB: Un unsername est unique pour chaque User
    rencontre = Rencontre.objects.filter(idRencontre=idRencontre)
    if not utilisateur_recipient:
        succes=False
        feedback = "Aucun joueur ne correspond à ce nom."
    elif not rencontre:
        succes=False
        feedback = "Aucune rencontre correspondant à cet id n'existe."
    else:
        joueur_sender = getJoueurConnecte(request)#C'est le joueur qui réalise la demande en Amis
        joueur_recipient = Joueur.objects.get(idJoueur=utilisateur_recipient[0])

        #Vérifions s'il existe déjà  une invitation de ce joueur pour cette rencontre
        integrity_inviter = Inviter.objects.filter(idJoueur=joueur_recipient,idRencontre=rencontre[0])

        #Vérifions s'il existe déjà une participation de ce joueur pour cette rencontre.
        participation = Participer.objects.filter(idJoueur=joueur_recipient,idRencontre=rencontre[0])

        if joueur_recipient.idJoueur==joueur_sender.idJoueur: #Un joueur ne peut pas s'ajouter en ami lui-même
            succes=False
            feedback = "Vous ne pouvez pas vous inviter."
        elif (not integrity_inviter) and (not participation): #Si aucune relation n'a été trouvée dans inviter ou participer
            invitation = Inviter(idJoueur=joueur_recipient,idRencontre=rencontre[0],joueurDemandeur=joueur_sender)
            invitation.save()
            succes=True
            feedback = "Votre invitation à été envoyée avec succès."
        else:
            succes=False
            feedback = utilisateur_recipient[0].username+" est déjà invité à cette rencontre."

    reponse = {
        "succes":succes,
        "feedback":feedback,
    }
    return JsonResponse(reponse)



#LIST
#Retourne toutes les invitations de la rencontre dont l'id est donné en paramètre
def listInvitationsRencontre(request,idRencontre):
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre)
    invitations = Inviter.objects.filter(idRencontre=rencontre)
    return invitations

#Retourne les invitations du joueur connecté
def listInvitationsJoueur(request):
    Joueur = getJoueurConnecte(request)
    invitations = Inviter.objects.filter(idJoueur=Joueur)
    return render(request, "inviter/list_invitationsJoueur.html", {"Invitations":invitations,})


#UPDATE
#Pas de mise à jour pour Inviter. Une invitation ne se modifie pas, il faut la supprimer et en créer une nouvelle.


#VALID
def acceptInviter(request):
    idRencontre = request.POST.get('idRencontre')  # Récupération de l'username

    rencontre = Rencontre.objects.filter(idRencontre=idRencontre)
    if not rencontre:
        succes = False
        feedback = "Cette rencontre n'existe pas."
    else:
        joueur = getJoueurConnecte(request)
        invitation = Inviter.objects.filter(idJoueur=joueur,idRencontre=rencontre[0])

        if not invitation: #Pas de rencontre trouvée
            succes="False"
            feedback = "Aucune invitation correspondant à cette rencontre n'a été trouvée."
        else: #Rencontre trouvée
            createParticiper(joueur, rencontre[0]) #Le joueur participe à la rencontre
            invitation[0].delete()  # On peut supprimer l'invitation désormais
            succes=True
            feedback = "Invitation acceptée !"

    reponse = {
        'succes' : succes,
        'feedback' : feedback,
    }
    return JsonResponse(reponse)


#Rejeter une invitation reçue
#Récupère le id du joueurDemandeur et l'id de la rencontre
#Fait ensuite appel à deleteInviter() en lui précisant le code de suppression
def rejeterInvitation(request):
    id_joueurDemandeur = request.POST.get('User')  # Récupération de l'id du joueur demandeur
    idRencontre = request.POST.get('idRencontre')  # Récupération de l'idRencontre
    codeSuppression = 0 #La suppression provient de la fonction rejeterInvitation
    return deleteInviter(request,id_joueurDemandeur,idRencontre,codeSuppression)


#Annuler une invitation envoyé
#Récupère le id du joueur invité (idJoueur) et l'id de la rencontre
#Fait ensuite appel à deleteInviter() en lui précisant le code de suppression
def annulerInvitation(request):
    id_joueurInvite = request.POST.get('User')  # Récupération de l'id du joueur invité
    idRencontre = request.POST.get('idRencontre')  # Récupération de l'idRencontre
    codeSuppression = 1 #La suppression provient de la fonction annulerInvitation
    return deleteInviter(request, id_joueurInvite, idRencontre, codeSuppression)

#DELETE
def deleteInviter(request,idJoueur,idRencontre,codeSuppression):
    utilisateur_autre = User.objects.filter(id=idJoueur)
    rencontre = Rencontre.objects.filter(idRencontre=idRencontre)

    if not utilisateur_autre:
        succes = False
        feedback = "Aucun joueur ne correspond à ce nom."
    elif not rencontre:
        succes = False
        feedback = "Aucune rencontre correspondant à cet id n'existe."
    else:

        joueur = getJoueurConnecte(request)
        joueurAutre = Joueur.objects.get(idJoueur=utilisateur_autre[0])

        #Deux personnes peuvent supprimer l'inviation : le joueur qui a reçu l'invitation et celui qui a envoyé l'invitation
        #Donc soit le joueur connecté est idJoueur, soit il est joueurDemandeur.

        if codeSuppression==0: #Si la demande de suppression provient de rejeterInvitation, alors idJoueur=getJoueurConnecte
            invitation = Inviter.objects.filter(Q(idJoueur=joueur,idRencontre=idRencontre,joueurDemandeur=joueurAutre))
        else:   #Si la demande de suppression provient de annulerInvitation, alors idJoueur=joueurAutre
            invitation = Inviter.objects.filter(idJoueur=joueurAutre, idRencontre=idRencontre, joueurDemandeur=joueur)

        if not invitation:
            succes = False
            feedback = "Aucune invitation correspondante existante."
        else:
            invitation[0].delete()
            succes = True
            feedback = "Invitation supprimé."

    reponse = {
        'succes' : succes,
        'feedback' : feedback,
    }
    return JsonResponse(reponse)



# ---- VIEWS PARTICIPER

#CREATE
#Prend en paramètre un joueur et une rencontre
#Cette fonction n'est pas accessible par l'utilisateur
#La création d'un participation ce fait de deux manière:
# 1-L'utilisateur organise une rencontre, il participe automatiquement à sa rencontre
# 2-L'utilisateur est invité, il valide son invitation et participe ainsi au match.
def createParticiper(joueur,rencontre):
    choix_equipe = random.choice(['LOC', 'VIS', ])  # L'équipe du joueur est décidée aléatoirement
    new_participer = Participer(idJoueur=joueur, idRencontre=rencontre, equipe=choix_equipe)
    new_participer.save()


#READ
#Prend en paramètre l'id de la rencontre dont on souhaite avoir la participation du joueur connecté
def readParticiper(request,idRencontre):
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre) #Récupère la rencontre dont l'id est en paramètre
    joueur = getJoueurConnecte(request) #Récupère le joueur associé à l'utilisateur
    participer = get_object_or_404(Participer, idJoueur=joueur, idRencontre=rencontre) #Récupère la participation du joueur à la rencontre
    return render(request, "participer/readParticiper.html", {"Participer":participer,})


#UPDATE
#La seule chose modifiable dans une participation est le nombre de buts marqué et le choix de l'équipe.
def updateParticiper(request,idRencontre):
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre) #Récupère la rencontre dont l'id est en paramètre
    joueur = getJoueurConnecte(request) #Récupère le joueur associé à l'utilisateur
    participer = get_object_or_404(Participer, idJoueur=joueur, idRencontre=rencontre) #Récupère la participation du joueur à la rencontre
    nbButs_possible = participer.idRencontre.dateRencontre >= date.today()  # Le joueur peut modifier son score uniquement si la date du match est passé ou actuelle

    if request.method == "POST":
        form = UpdateParticiperForm(request.POST)
        if form.is_valid():
            if nbButs_possible:
                participer.nombreButs = form.cleaned_data['nombreButs']
            else:
                participer.equipe = form.cleaned_data['equipe']
                participer.nombreButs = 0
                participer.save()
            return readRencontre(request,idRencontre)
    else:
        dataform = {
            "equipe":participer.equipe,
        }
        form = UpdateParticiperForm(dataform)
    return render(request, "participer/updateParticiper.html", {"UpdateParticiperForm":form,"Possible":nbButs_possible})


#DELETE
def deleteParticiper(request,idRencontre):
    rencontre = get_object_or_404(Rencontre, idRencontre=idRencontre) #Récupère la rencontre dont l'id est en paramètre
    joueur = getJoueurConnecte(request) #Récupère le joueur associé à l'utilisateur
    participer = get_object_or_404(Participer, idJoueur=joueur, idRencontre=rencontre) #Récupère la participation du joueur à la rencontre
    if request.method == "POST":
        participer.delete()
        return listRencontre(request)

    return render(request, "delete.html", {"ObjetDelete":participer})




# ---- VIEWS STADE

#CREATE
def createStade(request):
    if request.method == "POST":
        form = StadeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return listStade(request)
    else:
        form = StadeForm()

    return render(request, "stade/create_stade.html", {"StadeForm":form})


#READ
def readStade(request,idStade):
    stade = get_object_or_404(Stade, idStade=idStade)
    return render(request, "stade/read_stade.html", {"Stade":stade})


#LIST
def listStade(request,page=1):
    stades_list = Stade.objects.all()
    paginator = Paginator(stades_list, 3) #Affiche 3 stades par page

    stades = paginator.get_page(page)
    return render(request, 'stade/list_stade.html', {'stades': stades})

def listStadeMonQuartier(request,page=1):
    joueur= getJoueurConnecte(request)
    stades_list = Stade.objects.filter(quartierStade=joueur.quartierJoueur)
    paginator = Paginator(stades_list, 3) #Affiche 3 stades par page

    stades = paginator.get_page(page)
    return render(request, 'stade/list_stade.html', {'stades': stades})

#UPDATE
def updateStade(request,idStade):
    stade = get_object_or_404(Stade, idStade=idStade)
    if request.method == "POST":
        form = StadeForm(request.POST, request.FILES)
        if form.is_valid():
            stade.nomStade = form.cleaned_data['nomStade']
            stade.rueStade = form.cleaned_data['rueStade']
            stade.villeStade = form.cleaned_data['villeStade']
            stade.codepostalStade = form.cleaned_data['codepostalStade']
            stade.quartierStade = form.cleaned_data['quartierStade']
            stade.nombreTerrain = form.cleaned_data['nombreTerrain']
            stade.imageStade = form.cleaned_data['imageStade']
            stade.save()
            return readStade(request,stade.idStade)

    else:
        formdata = {
            "nomStade":stade.nomStade,
            "rueStade": stade.rueStade,
            "villeStade": stade.villeStade,
            "codepostalStade": stade.codepostalStade,
            "quartierStade": stade.quartierStade,
            "nombreTerrain": stade.nombreTerrain,
            "imageStade": stade.imageStade.url,
        }
        form = StadeForm(formdata)
    return render(request, "stade/create_stade.html", {"StadeForm":form})


#DELETE
def deleteStade(request,idStade):
    stade = get_object_or_404(Stade, idStade=idStade)
    if request.method == "DELETE":
        stade.delete()
        return listStade(request)
    return render(request, "delete.html", {"ObjetDelete":stade})




# ---- VIEWS QUARTIER
#CREATE
#READ
#UPDATE
#DELETE

#LES QUARTIERS SONT GÉRÉS PAR L'ADMINISTRATEUR.
#IL FAUT DONC UTILISER L'INTERFACE D'ADMINISTRATION DE DJANGO POUR REALISER CES ACTIONS (CRUD)


#LIST
#Retourne tous les quartiers
def listQuartier(request):
    quartier = Quartier.objects.all() #Récupère tous les quartiers
    return render(request, "quartier/listQuartier.html",{"Quartier":quartier})

