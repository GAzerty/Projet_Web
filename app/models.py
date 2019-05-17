from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator




#MODEL - QUARTIER
#La Création et Suppression de Quartier est uniquement disponible pour l'administrateur dans son interface
class Quartier(models.Model):
    idQuartier = models.AutoField(primary_key=True) #Clé primaire, s'incrèmente à chaque création
    nomQuartier = models.CharField(max_length=255)

    class Meta:
        db_table = "quartier"   #Le nom attribué en base de données

    #Définit l'affichage d'un quartier en Template, équivalent à toString
    def __str__(self):
        return self.nomQuartier







#MODEL - Joueur
class Joueur(models.Model):
    idJoueur = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    quartierJoueur = models.ForeignKey('Quartier',on_delete=models.CASCADE)

    class Meta:
        db_table = "joueur"     #Le nom attribué en base de données

#on_delete models.CASCADE : equivalent à la commande SQL, supprime par la même occasion tout ce qui dépend  de l'élément supprimé
#Le OneToOneField correspond à une clé étrangère (foreign key) mais on l'utilise surtout pour une notion d'héritage entre modèles
#Ici un Joueur est un User (définit par Django)


#MODEL - AMIS
class Amis(models.Model):
    Attendre = 'AT'
    Accepter = 'AC'
    ETAT_CHOIX = (
        (Attendre, 'Attente'),
        (Accepter, 'Accepter'),
    )
    #Si le joueur refuse la demande d'amis alors la demande est supprimé de la bd, cette action n'est pas géré ici

    joueur1Amis = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_sender') #Le joueur qui fait la demande en amis. ForeignKey pour définit l'attribut comme clé étrangère de Joueur
    joueur2Amis = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_recipient') #Le joueur qui reçoit la demande en amis
    etatJoueur1 = models.CharField(max_length=2, choices=ETAT_CHOIX, default=Accepter) #Par défaut le joueur qui demande Accepte
    etatJoueur2 = models.CharField(max_length=2, choices=ETAT_CHOIX, default=Attendre) #Par défaut le joueur qui reçoit est en Attente

    class Meta:
        db_table = "amis"   #Le nom attribué en base de données
        constraints = [
            models.UniqueConstraint(fields=['joueur1Amis', 'joueur2Amis'], name='amis_unique'),
        ]
        #Les attributs joueur1Amis et joueur2Amis sont clés primaires ensemble


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
    scoreVisiteurs = models.IntegerField(blank=True,default=0) #Blank = True indique que l'attribut n'est pas obligatoire en formulaire
    lieuRencontre = models.ForeignKey('Stade',on_delete=models.CASCADE)
    dateRencontre = models.DateField()
    heureRencontre = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(2359)]) #Trigger pour arrondir les minutes de l'heure du match : 15h28 -> 15h30
    #Ajout de validators sur le Min et Max de l'attribut heureRencontre pour s'assurer de possèder des heures significatives
    class Meta:
        db_table = "rencontre"      #Le nom attribué en base de données


    #Retourne l'heure de la rencontre au format Heures+'h'+"Minutes: 1220 -> 12h20
    def toString_Heure(self):
        StrHeure = str(self.heureRencontre)[0:2]+"h"+str(self.heureRencontre)[2:4]
        return StrHeure







#MODEL - INVITER
class Inviter(models.Model):
    idJoueur = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_guest')#Le joueur invité au match, on ajoute un related_name afin d'évitez les conflits
    idRencontre = models.ForeignKey('Rencontre', on_delete=models.CASCADE)
    joueurDemandeur = models.ForeignKey('Joueur', on_delete=models.CASCADE, related_name='joueur_invite')#Le joueur qui réalise l'inivtation

    class Meta:
        db_table = "inviter"        #Le nom attribué en base de données
        constraints = [
            models.UniqueConstraint(fields=['idJoueur', 'idRencontre'], name='inviter_unique'),
        ]

    #Les attributs idJoueur et idRencontre sont clés primaires ensembles





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
    nombreButs = models.IntegerField(blank=True, default=0, validators=[MinValueValidator(0)]) #Ajout d'un validator sur la valeur minimale du nombre de buts marqué avant que ce dernier soit ajouté en base de données
    equipe = models.CharField(max_length=3,choices=EQUIPE_CHOIX)        #Le joueur est soit dans l'équipe Visiteurs soit Locaux

    class Meta:
        db_table = "participer"
        constraints = [
            models.UniqueConstraint(fields=['idJoueur', 'idRencontre'], name='participer_unique'),
        ]

    # Les attributs idJoueur et idRencontre sont clés primaires ensembles



#MODEL - STADE
#La Création et Suppression de Stade est uniquement disponible pour l'administrateur dans son interface
class Stade(models.Model):
    idStade = models.AutoField(primary_key=True)
    nomStade = models.CharField(max_length=255)
    rueStade = models.CharField(max_length=255)
    villeStade = models.CharField(max_length=255)
    codepostalStade = models.IntegerField()
    quartierStade = models.ForeignKey('Quartier',on_delete=models.CASCADE)
    nombreTerrain = models.IntegerField(validators=[MinValueValidator(1)])
    imageStade = models.ImageField(upload_to='stades/')     #ImageField prend en paramètre avec upload_to le répertoire dans lequel le fichier sera stocké.
    #On accède à l'image en Template avec le suffixe imageStade.url (dans le src d'une balise img), cela renvoie l'url à laquelle l'image se trouve pour pouvoir l'affiché

    class Meta:
        db_table = "stade"

    def __str__(self):
        return self.nomStade