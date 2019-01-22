from othello.piece import Piece

from itertools import product


class Planche:
    """
    Classe représentant la planche d'un jeu d'Othello.
    """

    def __init__(self):
        """
        Méthode spéciale initialisant une nouvelle planche.
        """
        # Dictionnaire de cases. La clé est une position (ligne, colonne), et la valeur une instance de la classe Piece.
        self.cases = {}

        # Appel de la méthode qui initialise une planche par défaut.
        self.initialiser_planche_par_default()

        # On joue au Othello 8x8
        self.nb_cases = 8

    def get_piece(self, position):
        """
        Récupère une pièce dans la planche.

        :param position: La position où récupérer la pièce.
        :type position: Tuple de coordonnées matricielles (ligne, colonne).
        :return: La pièce à cette position s'il y en a une, None autrement.
        """
        if position not in self.cases.keys():
            return None

        return self.cases[position]

    def position_valide(self, position):
        """
        Vérifie si une position est valide (chaque coordonnée doit être dans les bornes).

        :param position: Un couple (ligne, colonne).
        :type position: tuple de deux éléments
        :return: True si la position est valide, False autrement
        """
        return 0 <= position[0] < self.nb_cases and 0 <= position[1] < self.nb_cases

    def obtenir_positions_mangees(self, position, couleur):
        """
        Détermine quelles positions seront mangées si un coup de la couleur passée est joué à la position passée.

        ***RETOURNEZ SEULEMENT LA LISTE DES POSITIONS MANGÉES, NE FAITES PAS APPEL À piece.echange_couleur() ICI.***

        Ici, commencez par considérer que, pour la position évaluée, des pièces peuvent être mangées dans 8 directions
        distinctes représentant les 8 cases qui entourent la position évaluée. Vous devez donc vérifier, pour chacune
        de ces directions, combien de pièces sont mangées et retourner une liste regroupant les pièces mangées dans
        toutes les directions.

        Pensez à faire appel à la fonction obtenir_positions_mangees_direction().

        :param position: La position du coup à jouer.
        :param couleur: La couleur du coup à jouer.
        :return: une liste contenant toutes les positions qui seraient mangées par le coup.
        """
        positions_mangees = []

        directions = list(product([-1, 0, 1], [-1, 0, 1]))
        directions.remove((0, 0))

        for d in directions:
            positions_mangees += self.obtenir_positions_mangees_direction(couleur, d, position)

        return positions_mangees

    def obtenir_positions_mangees_direction(self, couleur, direction, position):
        """
        Détermine les positions qui seront mangées si un coup de couleur "couleur" est joué à la position "position",
        si on parcourt la planche dans une direction "direction".

        Pour une direction donnée, vous devez parcourir la planche de jeu dans la direction. Tant que votre déplacement
        vous mène sur une pièce de la couleur mangée, vous continuez de vous déplacer. Trois situations surviennent
        alors pour mettre un terme au parours dans la direction :

        1) Vous arrivez sur une case vide. Dans ce cas, aucune pièce n'est mangée.

        2) Vous arrivez sur une case extérieure à la planche. Encore une fois, aucune pièce n'est mangée.

        3) Vous arrivez sur une case de la même couleur que le coup initial. Toutes les pièces de la couleur opposée
        que vous avez alors rencontrées dans votre parcours doivent alors être ajoutées à grande liste des pièces
        mangées cumulées.

        N.B. : Cette méthode peut être implémentée par au moins deux techniques différentes alors laissez place à votre
        imagination et explorez ! Une méthode faisant une boucle d'exploration complète et une méthode de parcours
        récursif  sont quelques-unes des façons de faire que vous pouvez explorer. Il se peut même que votre solution
        ne soit pas dans les solutions énumérées précédemment.

        :param couleur: La couleur du coup évalué
        :param direction: La direction de parcours évaluée
        :param position: La position du coup évalué
        :return: La liste (peut-être vide) de toutes les positions mangées à partir du coup et de la direction donnés.
        """
        couleur_mangee = "blanc" if couleur == "noir" else "noir"

        position_tentee = (position[0] + direction[0], position[1] + direction[1])
        positions_potentiellement_mangees = []

        while True:
            piece = self.get_piece(position_tentee)

            if piece is None:
                break
            else:
                if piece.couleur == couleur_mangee:
                    positions_potentiellement_mangees.append(position_tentee)
                else:
                    return positions_potentiellement_mangees

            position_tentee = (position_tentee[0] + direction[0], position_tentee[1] + direction[1])

        return []

    def coup_est_possible(self, position, couleur):
        """
        Détermine si un coup est possible. Un coup est possible si au moins une pièce est mangée par celui-ci et
        s'il n'y a pas déjà de pièce à la position désirée.

        :param position: La position du coup évalué
        :param couleur: La couleur du coup évalué
        :return: True, si le coup est valide, False sinon
        """
        return len(self.obtenir_positions_mangees(position, couleur)) > 0 and position not in self.cases.keys()

    def lister_coups_possibles_de_couleur(self, couleur):
        """
        Fonction retournant la liste des coups possibles d'une certaine couleur. Un coup est considéré possible
        si au moins une pièce est mangée quand la couleur "couleur" joue à une certaine position, ne l'oubliez pas!

        ATTENTION: ne dupliquez pas de code déjà écrit! Réutilisez les fonctions déjà programmées!

        :param couleur: La couleur ("blanc", "noir") des pièces dont on considère le déplacement.
        :type couleur: string
        :return: Une liste de positions de coups possibles pour la couleur "couleur"
        """
        coups_possibles = []

        for position in list(product(range(self.nb_cases), range(self.nb_cases))):
            if position not in self.cases.keys():
                if self.coup_est_possible(position, couleur):
                    coups_possibles.append(position)

        return coups_possibles

    def jouer_coup(self,position,couleur):
        """
        Joue une pièce de la couleur "couleur" à la position "position".

        Cette méthode doit également:
        - Ajouter la pièce aux pièces de la planche.
        - Faire les changements de couleur pour les pièces mangées par le coup.
        - Retourner un message indiquant "ok" ou "erreur".

        ATTENTION: Ne dupliquez pas de code! Vous avez déjà une méthode qui valide si un coup est possible, appelez la !

        :param position: La position du coup.
        :param couleur: La couleur du coup.
        :return: "ok" si le déplacement a été effectué car il est valide, "erreur" autrement.
        """

        if not self.coup_est_possible(position, couleur):
            return "erreur"

        positions_mangees = self.obtenir_positions_mangees(position, couleur)

        self.cases[position] = Piece(couleur)

        for p in positions_mangees:
            self.get_piece(p).echange_couleur()

        return "ok"

    def convertir_en_chaine(self):
        """
        Retourne une chaîne de caractères où chaque case est écrite sur une ligne distincte.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        Cette méthode pourrait par la suite être réutilisée pour sauvegarder une planche dans un fichier.

        :return: La chaîne de caractères.
        """
        chaine = ""
        for position, piece in self.cases.items():
            chaine += "{},{},{}\n".format(position[0], position[1], piece.couleur)

        return chaine

    def charger_dune_chaine(self, chaine):
        """
        Remplit la planche à partir d'une chaîne de caractères comportant l'information d'une pièce sur chaque ligne.
        Chaque ligne contient l'information suivante :
        ligne,colonne,couleur

        :param chaine: La chaîne de caractères.
        :type chaine: string
        """
        self.cases.clear()
        for information_piece in chaine.split("\n"):
            if information_piece != "":
                ligne_string, colonne_string, couleur = information_piece.split(",")
                self.cases[(int(ligne_string), int(colonne_string))] = Piece(couleur)

    def initialiser_planche_par_default(self):
        """
        Initialise une planche de base avec la position initiale des pièces.
        """
        self.cases.clear()
        self.cases[(3, 3)] = Piece("blanc")
        self.cases[(3, 4)] = Piece("noir")
        self.cases[(4, 3)] = Piece("noir")
        self.cases[(4, 4)] = Piece("blanc")

    def __repr__(self):
        """
        Cette méthode spéciale permet de modifier le comportement d'une instance de la classe Planche pour l'affichage.
        Faire un print(une_planche) affichera la planche à l'écran.
        """
        s = "  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"
        for i in range(0, self.nb_cases):
            s += str(i)+" | "
            for j in range(0, self.nb_cases):
                if (i, j) in self.cases:
                    s += str(self.cases[(i, j)])+" | "
                else:
                    s += "  | "
            s += str(i)
            if i != self.nb_cases - 1:
                s += "\n  +---+---+---+---+---+---+---+---+\n"

        s += "\n  +-0-+-1-+-2-+-3-+-4-+-5-+-6-+-7-+\n"

        return s