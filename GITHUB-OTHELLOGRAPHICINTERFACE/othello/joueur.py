from random import choice


class Joueur:
    """
    Classe générale de joueur. Vous est fournie.
    """

    def __init__(self, couleur):
        """
        Le constructeur global de Joueur.

        :param couleur: La couleur qui sera jouée par le joueur.
        """
        assert couleur in ["blanc", "noir"], "Piece: couleur invalide."

        self.couleur = couleur

    def obtenir_type_joueur(self):
        '''
        Cette méthode sera utilisée par les sous-classes JoueurHumain et JoueurOrdinateur.

        :return: 'Ordinateur' ou 'Humain'
        '''
        pass

    def choisir_coup(self, coups_possibles):
        '''
        Cette méthode sera implémentée par les sous-classes JoueurHumain et JoueurOrdinateur.

        :param coups_possibles: la liste des coups possibles
        :return: un couple (ligne, colonne) représentant la positon du coup désiré.
        '''
        pass


class JoueurHumain(Joueur):
    """
    Classe modélisant un joueur humain.
    """

    def __init__(self, couleur):
        """
        Cette méthode va construire un objet Joueur et l'initialiser avec la bonne couleur.
        """
        super().__init__(couleur)

    def obtenir_type_joueur(self):
        return "Humain"

    def choisir_coup(self, coups_possibles):
        """
        Demande successivement à l'usager à quelle ligne, puis à quelle colonne il désire jouer.

        Nous vous avons déjà fourni une portion de code permettant d'attrapper au passage les erreurs qui peuvent
        survenir lorsque l'utilisateur entre autre chose qu'un nombre entier.

        :param coups_possibles: La liste des coups possibles
        :return: un couple (ligne, colonne) représentant la position du coup désiré.
        """
        try:
            # Votre code doit être ici, entre try: et except
            print("(Position coup) Numéro de ligne: ", end="")
            coup_ligne = int(input())
            print("(Position coup) Numéro de colonne: ", end="")
            coup_colonne = int(input())

            return (coup_ligne, coup_colonne)

        except ValueError:
            # L'usager a fait une erreur de saisie, on retourne donc un coup que l'on sait invalide
            print("Position invalide.\n")
            print("")
            return (-1, -1)


class JoueurOrdinateur(Joueur):
    """
    Classe modélisant un joueur Ordinateur.
    """
    def __init__(self, couleur):
        """
        Cette méthode va construire un objet Joueur et l'initialiser avec la bonne couleur.
        """
        super().__init__(couleur)

    def obtenir_type_joueur(self):
        return "Ordinateur"

    def choisir_coup(self, coups_possibles):
        """
        Pour votre joueur ordinateur, vous n'avez qu'à sélectionner un coup au hasard parmi la liste des coups
        possibles. Affichez ensuite en console les numéros de ligne et de colonne.

        Pour faire un choix au hasard, vous devrez faire appel à la libraire random de Python. Explorez là, elle
        possède même une fonction retournant précisément un choix aléatoire parmi une liste.

        :param coups_possibles: La liste des coups possibles
        :return: un couple (ligne, colonne) représentant la position du coup désiré.
        """
        coup = choice(coups_possibles)

        print("(Position coup) Numéro de ligne:", coup[0])
        print("(Position coup) Numéro de colonne:", coup[1], "\n")

        return coup
