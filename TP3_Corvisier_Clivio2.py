import random
import math

#TP3, par Jean-Christophe Corvisier et Oscar Clivio.
directions = {
"N": (-1, 0),
"S": ( 1, 0),
"E": ( 0, 1),
"W": ( 0, -1),
"NE": (-1, 1),
"NW": (-1, -1),
"SE": ( 1, 1),
"SW": ( 1, -1)
}


#Tableau contenant les différents "coups" possibles qui seront utilisés
#par la suite
direct=[(-1,0),(1,0),(0,1),(0,-1),(-1,1),(1,1),(1,-1)]


#Définition des exceptions

class TaillePasInt(Exception): pass

class MauvaiseValeurTaille(Exception): pass
        
class NomPasStr(Exception): pass

class TypeJeuPasBool(Exception): pass

#Classes utiles pour le jeu: grille, joueur, jeu.

class Grid:
    def __init__(self, donnee):
        """
        Vérifie que la donnée entrée est au bon format puis initialise la
        grille. Attributs initialisés: taille _taille et  données _elements de
        la grille.
        """
        #PREMIER CAS: la donnée entrée est un str, c'est un fichier, et on
        #le charge. On suppose que lorsque le chargement réussit, le fichier
        #est au bon format (CSV, dimensions égales)
        if isinstance(donnee, str):
            try:
                with open(donnee, "r") as fichier:
                        Lignes = fichier.readlines()
                        #Mise à jour de la taille
                        self._taille = len(Lignes)
                        #Création de la grille sous forme de liste de liste
                        self._elements=[]
                        for i in range(len(Lignes)):
                            self._elements.append([])
                            #Suppression du "\n" à Lignes
                            Lignes[i] = Lignes[i].strip('\n')
                            #Séparation selon les ","
                            ValeursStr = Lignes[i].split(',')
                            for j in range(len(Lignes)):
                                self._elements[i].append( int(ValeursStr[j]) )
            except FileNotFoundError:
                print("Impossible d'ouvrir le fichier "+donnee)    
                print("Taille mise par défaut à 5, et les données à None")
                self._taille = 5
                #Création de la grille sous forme de liste de liste
                self._elements=[[None]*5 for i in range(5)]
                
        else: 
            #DEUXIEME CAS: la donnée entrée est en fait une taille. Elle doit
            #être au format int, impaire et positive.
            try:
                if not(isinstance(donnee, int)):
                    raise TaillePasInt
                if (donnee < 0 or donnee%2==0):
                    raise MauvaiseTaille
            except TaillePasInt:
                print("Taille de type différent de int")
                print("Taille mise par défaut à 5")
                donnee = 5
            except MauvaiseValeurTaille:
                print("Taille de valeur incorrecte: " + str(donnee))
                if (donnee < 0):
                    print("Taille rendue positive")
                    donnee = -donnee
                if (donnee%2 == 0):
                    print ("Taille incrémentée de 1 pour être impaire")
                    donnee += 1
                    print("Nouvelle taille: " + str(donnee))
            finally:
                #Création d'un champ taille de la grille
                self._taille=donnee
                #Création de la grille sous forme de liste de liste
                self._elements=[[None]*donnee for i in range(donnee)]
        
    @property
    def taille(self):
        """
        Renvoie la taille de la grille
        """
        return self._taille

    def __getitem__(self,Coords):
        """
        Prend un tuple et renvoie la valeur dans la grille associée à ce tuple.
        """
        (indice1,indice2)=Coords
        return self._elements[indice1][indice2]
    
    def __setitem__(self,Coords,valeur):
        """
        Remplace la valeur dans le tableau en position Coords par une autre
        valeur.
        """
        (indice1,indice2)=Coords
        self._elements[indice1][indice2]=valeur
        
    def __contains__(self,Coords):
        """
        Permet l'utilisation de l'opérateur in pour savoir si la case demandée
        est dans la grille.
        """
        (x,y)=Coords
        return ((x>=0 ) and (x<self._taille) and (y>=0) and (y<self._taille))
    
    def affiche(self):
        """
        Affiche la grille.
        """
        for i in range(self._taille):
            affichage=""
            for j in range(self._taille):
                #pour afficher de manière bien aligné les nombres et
                #le personnage, on utilise la petite opération suivante
                str_coords = str(self[(i,j)])
                affichage=affichage + " "*(5-len(str_coords)) + str(str_coords)
            print(affichage)

    def sauve(G, file_str):
        """
        Sauvegarde la grille au format CSV dans le fichier file_str
        """
        with open(file_str, "w") as fichier:
            try:
                for i in range(G.taille):
                    for j in range(G.taille):
                        StrNombre = str(G[(i,j)])
                        fichier.write(StrNombre)
                        if (j < G.taille-1):
                            fichier.write(",")
                    fichier.write('\n')
            except:
                print("Impossible de sauvegarder la grille !")
                exit(1)
                
    
    def maximum(self):
        """
        Calcule le maximum des éléments de la grille. Utile pour l'algorithme
        du min-max.
        """
        return max([max(ligne) for ligne in self._elements])
    

class Player:
    
    def __init__(self,nom):
        """
        Création des champs nom et du score initialisé à 0.
        Vérifie bien si le nom est un string.
        """
        try:
            if isinstance(nom, str):
                self._name = nom
            else:
                raise NomPasStr
        except NomPasStr:
            print("Un nom de joueur n'est pas de type str")
            print("Le nom en question est maintenant tiré au hasard")
            self._name = "Player_"+str(random.randint(0,100))
            print("Nouveau nom: "+self._name)
        finally:
            self._score=0
     
    @property
    def name(self):
        """
        Fonction qui renvoie le nom du joueur.
        """
        return self._name
    
    @property
    def score(self):
        """
        Fonction qui renvoie le score du joueur.
        """
        return self._score
        
    def incremente(self,valeur):
        """
        Fonction qui incrémente le score du joueur.
        """
        self._score += valeur
        
    def affichage_nom_score(self):
        """
        Fonction qui affiche le nom puis le score comme demandé dans l'énoncé.
        """
        affichage= self._name + " : " + str(self._score)
        print(affichage)

    
    def copie_joueur(self,joueur):
        """
        Copie dans self les informations du joueur donné en argument
        (utile pour MinMax)
        """
        self._name=joueur.name
        self._score=joueur.score

        
class Game:
    
    def __init__(self,donneegrille,nomplayer1,nomplayer2,joueravecIA):
        """
        Initialise le jeu; requiert une taille, les noms des deux joueurs,
        et un booléen signifiant si l'on joue contre l'IA ou non.
        Remarque: joueravecIA est un booléen qui indique si on désire jouer
        avec l'ordinateur ou non, nomplayer2 devient alors le nom que l'on
        donne à l'ordinateur.
        """
        try:
            if isinstance(joueravecIA, bool):
                self._joueavecIA = joueravecIA
            else:
                raise TypeJeuPasBool
        except TypeJeuPasBool:
            print("L'information sur jeu avec IA ou non n'est pas un bool")
            self._joueavecIA = bool(joueravecIA)
            print("Information convertie en bool: "+str(self._joueavecIA))
        finally:
            P1=Player(nomplayer1)
            P2=Player(nomplayer2)
        self._listejoueur=[P1,P2]
      
        #Création de la grille
        self._grille=Grid(donneegrille)
        taille = self._grille.taille
        #Personnage placé sur la case du milieu de la grille.
        self._positionperso=(taille//2,taille//2)
        
        #Liste des valeurs possibles pour les cases de la grille.
        listevaleurcase=[5,10,20,50,100,200]

        #Initialisation de la grille
        for i in range(taille):
            for j in range(taille):
                #On remplit les cases de la grille de manière aléatoire
                #avec des éléments de la liste des valeurs possibles.
                valeur = random.choice(listevaleurcase)
                self._grille[(i,j)] = valeur
    
        #Valeur élevée utile pour l'algorithme du min-max
        #Elle doit être supérieure à toute différence de score entre deux
        #joueurs, c'est-à-dire au score maximal qu'un joueur peut avoir,
        #c'est-à-dire celui qu'il a lorsqu'il parcourt toutes les cases,
        #ce score est donc inférieur au maximum des valeurs des cases multiplié
        #par la taille au carré
        self._grandevaleurMinMax = 10*taille*taille*self._grille.maximum()
    
        #place le personnage au centre de la grille
        self._grille[(taille//2,taille//2)] = "###"

        #On créée un champs contenant l'indice de la liste des joueurs qui
        #désigne le joueur qui doit jouer le coup à venir.
        #Par défaut on considère que le joueur 1 (indice 0) commence.
        self._numerojoueurcourant=0



    def direction(self):
        """
    Fonction qui entre et convertit les coups des joueurs.
    Pour jouer en haut, le joueur tape N comme North.
    Pour jouer en bas, il tape S comme South.
    Pour jouer à droite il joue E comme East.
    Pour jouer à gauche, W comme West.
    Pour joueur en haut à droite , NE.
    Pour jouer en bas à droite SE;
    Pour jouer en haut à gauche, NW.
    Pour jouer en bas à droite , SE.
       """
        direction_coup = None
        while direction_coup is None:
            coupjoueur = input("Entrez votre coup: ")
            print("\n")
            direction_coup = directions.get(coupjoueur, None)
        return direction_coup




    def jouer(self,Coords):
        """
        Crée la nouvelle position du joueur.
        """
        position=(Coords[0]+self._positionperso[0],
                  Coords[1]+self._positionperso[1])
        if (position in self._grille and (self._grille[position]!=0)):
            #On vérifie que cette position est dans la grille et qu'elle ne
            #contient pas 0.
            #On met 0 dans la case précédemment occupé par le personnage.
            self._grille[self._positionperso] = 0
            #Mise à jour de la position du personnage.
            self._positionperso=position
            #On incrémente le score du joueur jouant.
            self.joueur_courant().incremente(self._grille[position])
            #Change le numero du joueur qui doit jouer au coup suivant.
            self._numerojoueurcourant = (self._numerojoueurcourant+1)%2
            #On indique la position du perso sur la grille.
            self._grille[position] = "###"
            #Retournz True pour signifier que le coup jouer est correct.
            return True
        else:
            #On retourne que le coup n'est pas possible.
            return False

          
    def copie_jeu(self):
        """
        Renvoie une copie du jeu self. Fonction très utile dans l'algorithme
        du min-max.
        """
        #Variables créées pour alléger la ligne où on déclare le nouveau jeu
        taille = self._grille.taille
        joueurs = self._listejoueur
        joueravecIA = self._joueavecIA
        #Copie
        jeu=Game(taille,joueurs[0].name,joueurs[1].name,joueravecIA)
        jeu._positionperso=self._positionperso
        jeu._numerojoueurcourant=self._numerojoueurcourant
        #utilisation de copies via la méthode copie_joueur définie
        #dans la classe Player
        jeu._listejoueur[0].copie_joueur(self._listejoueur[0])
        jeu._listejoueur[1].copie_joueur(self._listejoueur[1])
        #Copie des valeurs de la grille
        for i in range(self._grille.taille):
            for j in range(self._grille.taille):
                jeu._grille[(i,j)] = self._grille[(i,j)]
        return jeu

    def affichage_jeu(self):
        """
        Affiche le jeu.
        """
        #Affichage de la grille.
        self._grille.affiche()
        print()
        #Affichage des joueurs et de leur score.
        self._listejoueur[0].affichage_nom_score()
        print()
        self._listejoueur[1].affichage_nom_score()
        print()
        
    def joueur_courant(self):
        """
        Renvoie le joueur courant.
        """
        return self._listejoueur[self._numerojoueurcourant]

    #fonction qui 
    def indicegagnant(self):
        """
        Renvoie l'indice du joueur gagnant, ou -1 dans le cas d'une partie
        nulle.
        """
        if(self.gameover()):
            if(self._listejoueur[0].score>self._listejoueur[1].score):
                return 0
            elif(self._listejoueur[0].score<self._listejoueur[1].score):
                return 1
            else:
                return -1
            
    def resultat(self):
        """
        Affiche les résultats.
        """
        #Affichage en cas de victoire du joueur 1.
        if(self._listejoueur[0].score>self._listejoueur[1].score):
            affichage=self._listejoueur[0].name + " " +"a gagne !"
            print(affichage)
        #Affichage en cas de victoire du joueur 2.
        if(self._listejoueur[0].score<self._listejoueur[1].score):
            affichage=self._listejoueur[1].name + " " +"a gagne !"
            print(affichage)
        #Affichge en cas de partie nulle.
        if(self._listejoueur[0].score==self._listejoueur[1].score):
            affichage="Partie nulle"
            print(affichage)

    def gameover(self):
        """
        Vérifie si le jeu est terminé ou non.
        """
        #Creation des positions possibles.
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                (x,y)=self._positionperso
                Coords=(x+i,y+j)
                if (Coords in self._grille and (Coords !=(x,y))):
                     #si la case est dans la grille et vaut 0 le jeu continue.
                    if self._grille[Coords]!=0:
                        return False
        #Si aucune case ne peut être jouée le jeu s'arrête.
        return True

    def play(self):
        """
        fonction qui fait tourner le jeu, il prend en compte le fait que l'on
        affronte l'IA ou non
        """
        #Si on joue contre l'IA on peut choisir le niveau de difficulté
        level=0
        listeniveau=range(1,8)
        while(self._joueavecIA and (not(level in listeniveau))):
            print("Veuillez choisir un niveau de difficulté entre 1 et 7, ")
            print("7 étant le plus difficile : ")
            level=int(input(""))
            print("\n")
        #Jeu en lui-même
        while not(self.gameover()):
            self.affichage_jeu()
            print(self.joueur_courant().name + " doit jouer")
            #booléen indiquant si le joueur 1 a joue un coup correct ou non
            Coupcorrect= False
            #on demande au joueur 1 un coup tant que celui donné avant
            #n'est pas valide
            while(not(Coupcorrect)):
                Coupcorrect=self.jouer(self.direction())
                #affichage de la grille pour le joueur 1
                self.affichage_jeu()
                
            #dans le cas de l'IA jouant, on utilise la méthode minmax pour
            #trouver le meilleur coup en fonction de la profondeur par défaut
            if(self._joueavecIA):
                (valeur,coup)=self.min_max(level,True)        
                self.jouer(coup)
        self.affichage_jeu()
        self.resultat()                

        
    def min_max(self,profondeur,is_max):
        """
        La méthode principale de l'IA, transcription de l'algorithme MinMax.
        Ici, nous choisissons de retourner une évaluation qui correspond à la
        différence entre le score de l'IA et du joueur 1, dans cet algorithme
        MinMax, l'IA cherche donc à maximiser cette évaluation et le joueur à
        la minimiser.
        Pour éviter que l'ordinateur ne choisisse d'augmenter l'évaluation au
        détriment de la volonté de gagner, nous modifions la fonction
        d'évaluation de sorte que lorsque la partie est finie, une position
        gagnante pour l'IA renvoie un très bon score et une position
        gagnante pour le joueur un très mauvais score, le cas partie nulle
        est traité en renvoyant la différence des deux scores
        Comme nous cherchons à trouver un coup pour l'IA, la fonction MinMAx
        renvoie un couple comprenant l'évaluation et le meilleur coup à jouer
        à chaque étape de la récursivité.
        """
            
        #étape de fin de récursivité, évaluation de la position
        if(self.gameover() or (profondeur<1)):
            #on regarde ici si il s'agit du joueur  qui gagne
            
            #on renvoie dans ce cas une évaluation très mauvaise, et qui
            #l'est d'autant plus que le nombre de coups nécessaire pour y
            #parvenir est faible
            if(self.indicegagnant==0):
                return -self._grandevaleurMinMax-profondeur
                
            #cas de l'IA gagnante, on renvoie une évaluation très bonne,
            #et qui l'est d'autant plus que le nombre de coups nécessaire pour
            #y parvenir est faible
        
            elif(self.indicegagnant==1):
                return self._grandevaleurMinMax+profondeur
                
            #cas quelconque (inclue la partie nulle) on renvoie la différence
            #des scores
            
            else:
                evalue = self._listejoueur[1].score-self._listejoueur[0].score
                return (evalue,(0,0))
        else:
            #Copie préalable du jeu pour faire la descente récursive sans
            #problème
            JEU=self.copie_jeu()
            #cas de l'IA qui cherche à maximiser son gain
            
            if(is_max==True):
                #initialisation des deux éléments du couple réponse
                valeur=-math.inf
                coupjouer=(0,0)
                #recherche du meilleur coup pour l'IA
                for direction in direct:
                    #vérification que le coup est correct, si oui
                    #automatiquement le jeu est mis à jour
                    
                    if(JEU.jouer(direction)):
                        #appel récursif
                        (valeurcoup,coupj)=JEU.min_max(profondeur-1,False)
                        # si la valeur trouvée est plus grande que celle en
                        #mémoire, on retient le coup correspondant (c'est le
                        #meilleur gardé en mémoire)
                        if(valeurcoup>=valeur):
                            valeur=valeurcoup
                            coupjouer=direction
                    #Très important, on réinitialise le jeu tel qu'il était
                    #avant le début de la boucle sur les directions
                            
                    JEU=self.copie_jeu()
                return (valeur,coupjouer)
            else:#cas du joueur, il veut minimiser son gain
                valeur=math.inf
                coupjouer=(0,0)
                for direction in direct:
                    if(JEU.jouer(direction)):
                        (valeurcoup,coupj)=JEU.min_max(profondeur-1,True)
                        if(valeurcoup<=valeur):
                            valeur=valeurcoup
                            coupjouer=direction
                    JEU=self.copie_jeu()
                return (valeur,coupjouer)


#Jouer:
#Données correctes
g = Game(15,"Joueur","IA",True)
#En chargeant une grille prédéfinie
#g = Game("CSVFile.txt","Joueur","IA",True)
#Données délirantes, traitées par les exceptions
#g = Game(Grid(1),4,3,Grid(1))
g.play()
        
    

