from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


#MODEL - QUARTIER
class Quartier(models.Model):
    idQuartier = models.AutoField(primary_key=True)
    nomQuartier = models.CharField(max_length=255)

    class Meta:
        db_table = "quartier"

    def __str__(self):
        return self.nomQuartier

#MODEL - Joueur
class Joueur(models.Model):
    idJoueur = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    quartierJoueur = models.ForeignKey('Quartier',on_delete=models.CASCADE) #on_delete models.CASCADE : equivalent à la commande SQL

    class Meta:
        db_table = "joueur"


#MODEL - AMIS
class Amis(models.Model):
    Attendre = 'AT'
    Accepter = 'AC'
    ETAT_CHOIX = (
        (Attendre, 'Attente'),
        (Accepter, 'Accepter'),
    )
    #Si le joueur refuse la demande d'amis alors la demande est supprimé de la bd, cette action n'est pas géré ici

    joueur1Amis = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_sender') #Le joueur qui fait la demande en amis
    joueur2Amis = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_recipient') #Le joueur qui reçoit la demande en amis
    etatJoueur1 = models.CharField(max_length=2, choices=ETAT_CHOIX, default=Accepter)
    etatJoueur2 = models.CharField(max_length=2, choices=ETAT_CHOIX, default=Attendre)

    class Meta:
        db_table = "amis"
        constraints = [
            models.UniqueConstraint(fields=['joueur1Amis', 'joueur2Amis'], name='amis_unique'),
        ]


    #Retourne True si etatJoueur1 et etatJoueur2 sont Accepter
    def amitie_valide(self):
        return (self.etatJoueur1=='AC') and (self.etatJoueur2=='AC')

    #Retourne le joueur ami avec le joueur passé en paramètre
    def monAmi(self,Joueurconnecte):
        if self.joueur1Amis == Joueurconnecte:
            return self.joueur2Amis
        return self.joueur1Amis

#MODEL - RENCONTRE
class Rencontre(models.Model):
    idRencontre = models.AutoField(primary_key=True)
    scoreLocaux = models.IntegerField(blank=True,default=0) #Trigger pour determiner le scorelocaux et scorevisiteurs, en fonction des buts marqués des joueur lors du match
    scoreVisiteurs = models.IntegerField(blank=True,default=0)
    lieuRencontre = models.ForeignKey('Stade',on_delete=models.CASCADE)
    dateRencontre = models.DateField()
    heureRencontre = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(2359)])
    class Meta:
        db_table = "rencontre"


    #Retourne l'heure de la rencontre au format Heures+'h'+"Minutes
    def toString_Heure(self):
        StrHeure = str(self.heureRencontre)[0:2]+"h"+str(self.heureRencontre)[2:4]
        return StrHeure


#MODEL - INVITER
class Inviter(models.Model):
    idJoueur = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_guest')#Le joueur invité au match, on ajoute un related_name afin d'évitez les conflits
    idRencontre = models.ForeignKey('Rencontre', on_delete=models.CASCADE)
    joueurDemandeur = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_invite')#Le joueur qui réalise l'inivtation

    class Meta:
        db_table = "inviter"
        constraints = [
            models.UniqueConstraint(fields=['idJoueur', 'idRencontre'], name='inviter_unique'),
        ]



#MODEL - PARTICIPER
class Participer(models.Model):

    #Choix de l'équipe du joueur
    Locaux = 'LOC'
    Visiteurs = 'VIS'
    EQUIPE_CHOIX = (
        (Locaux,'Locaux'),
        (Visiteurs,'Visiteurs')
    )

    idJoueur = models.ForeignKey('Joueur', on_delete=models.CASCADE)
    idRencontre = models.ForeignKey('Rencontre', on_delete=models.CASCADE)
    nombreButs = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(0)])
    equipe = models.CharField(max_length=3,choices=EQUIPE_CHOIX)

    class Meta:
        db_table = "participer"
        constraints = [
            models.UniqueConstraint(fields=['idJoueur', 'idRencontre'], name='participer_unique'),
        ]




#MODEL - STADE
class Stade(models.Model):
    idStade = models.AutoField(primary_key=True)
    nomStade = models.CharField(max_length=255)
    rueStade = models.CharField(max_length=255)
    villeStade = models.CharField(max_length=255)
    codepostalStade = models.IntegerField()
    quartierStade = models.ForeignKey('Quartier',on_delete=models.CASCADE)
    nombreTerrain = models.IntegerField(validators=[MinValueValidator(1)])
    imageStade = models.ImageField(upload_to='stades/')
    class Meta:
        db_table = "stade"

    def __str__(self):
        return self.nomStade