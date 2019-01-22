
from tkinter import Tk, Canvas, Label, NSEW, messagebox
from othello.partie import Partie
from othello.planche import Planche
class CanvasPlanche(Canvas):
    """Classe héritant d'un Canvas, et affichant un échiquier qui se redimensionne automatique lorsque
    la fenêtre est étirée.

    """
    def __init__(self, parent, n_pixels_par_case):
        # Nombre de lignes et de colonnes.
        self.n_lignes = 8

        self.n_colonnes = 8

        self.n_pixels_par_case = n_pixels_par_case

        #pour localiser la postion

        self.chiffres_rangees = ['0','1','2','3','4','5','6','7']

        self.chiffres_colonnes = ['0','1','2','3','4','5','6','7']







        # Appel du constructeur de la classe de base (Canvas).
        # La largeur et la hauteur sont déterminés en fonction du nombre de cases.
        super().__init__(parent, width=self.n_lignes * n_pixels_par_case,
                         height=self.n_colonnes * self.n_pixels_par_case)

        # Dictionnaire contenant les pièces.

        self.pieces = {'34': 'blanc', '43': 'blanc', '44': 'noir', '33': 'noir'}

        # On fait en sorte que le redimensionnement du canvas redimensionne son contenu. Cet événement étant également
        # généré lors de la création de la fenêtre, nous n'avons pas à dessiner les cases et les pièces dans le
        # constructeur.
        self.bind('<Configure>', self.redimensionner)



    def dessiner_cases(self):
        """Méthode qui dessine les cases de la planche.

        """
        for i in range(self.n_lignes):
            for j in range(self.n_colonnes):
                debut_ligne = i*self.n_pixels_par_case
                fin_ligne = debut_ligne + self.n_pixels_par_case
                debut_colonne = j*self.n_pixels_par_case
                fin_colonne = debut_colonne + self.n_pixels_par_case

                # On dessine le rectangle. On utilise l'attribut "tags" pour être en mesure de récupérer les éléments

                self.create_rectangle(debut_colonne, debut_ligne, fin_colonne, fin_ligne, fill="dark green", tags='case')

    def dessiner_pieces(self):

        self.delete('piece')
        # Caractères unicode représentant les pièces. Police deja vu
        caracteres_pieces = {'blanc': '\u26C0', 'noir': '\u26C2​'}


        # Pour tout paire position, pièce:
        for position, piece in self.pieces.items():
            # On dessine la pièce dans le canvas, au centre de la case. On utilise l'attribut "tags" pour être en
            # mesure de récupérer les éléments dans le canvas.
            coordonnee_y = (self.n_lignes - self.chiffres_rangees.index(position[1]) - 1) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            coordonnee_x = self.chiffres_colonnes.index(position[0]) * self.n_pixels_par_case + self.n_pixels_par_case // 2
            self.create_text(coordonnee_x, coordonnee_y, text=caracteres_pieces[piece],
                             font=('Deja Vu', self.n_pixels_par_case//2), tags='piece')

    def redimensionner(self, event):
        # Nous recevons dans le "event" la nouvelle dimension dans les attributs width et height. On veut un damier
        # carré, alors on ne conserve que la plus petite de ces deux valeurs.
        nouvelle_taille = min(event.width, event.height)

        # Calcul de la nouvelle dimension des cases.
        self.n_pixels_par_case = nouvelle_taille // self.n_lignes

        # On supprime les anciennes cases et on ajoute les nouvelles.
        self.delete('case')
        self.dessiner_cases()

        # On supprime les anciennes pièces et on ajoute les nouvelles.
        self.delete('piece')
        self.dessiner_pieces()


class Fenetre(Tk):
    def __init__(self):
        super().__init__()
        self.planche = Planche()
        self.partie = Partie()

        # decommenter si on veut charger une partie et inserer le nom du fichier texte.

        #self.partie = Partie('partie_un_tour_a_passer.txt')

        # Nom de la fenêtre.
        self.title("Othello")

        # La position sélectionnée.
        self.position_selectionnee = None

        # Truc pour le redimensionnement automatique des éléments de la fenêtre.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Création du canvas_planche.
        self.canvas_planche = CanvasPlanche(self, 60)
        self.canvas_planche.grid(sticky=NSEW)

        # Ajout d'une étiquette d'information.
        self.messages = Label(self)
        self.messages.grid()

        # On lie un clic sur canvas_planche à une méthode.
        self.canvas_planche.bind('<Button-1>', self.selectionner)
        self.canvas_planche.pieces = self.convertir_case_a_piece()


    # Methode qui convertira le dictionnaire de case du jeu console sous le bon format
    def convertir_case_a_piece(self):

        piece = {}
        for key,values in self.partie.planche.cases.items():
            piece[str(key[0]) + str(key[1])] = values.couleur

        return piece




    def selectionner(self, event):
        # On trouve le numéro de ligne/colonne en divisant les positions en y/x par le nombre de pixels par case.
        ligne = event.y // self.canvas_planche.n_pixels_par_case
        colonne = event.x // self.canvas_planche.n_pixels_par_case
        position_message = "{}{}".format(self.canvas_planche.chiffres_colonnes[colonne],
                                 (self.canvas_planche.chiffres_rangees[self.canvas_planche.n_lignes - ligne - 1]))

        position = (int(self.canvas_planche.chiffres_colonnes[colonne]),int(self.canvas_planche.chiffres_rangees[self.canvas_planche.n_lignes - ligne - 1]))




        # On récupère l'information sur la pièce à l'endroit choisi. On traite les erreurs

        try:
            piece = self.canvas_planche.pieces[position_message]

            # On change la valeur de l'attribut position_selectionnee.

            self.position_selectionnee = position_message





        except KeyError:

            # retourne message derreur si coup invalide.
            if self.partie.jouer(position):
                message = messagebox.showinfo(' COUP INVALIDE',
                                              'POSITION INVALIDE: une piece inseree a cette position ne peut pas faire de prise')


            # on place les nouvelles piece jouer sur la planche en rafraichissant celle-ci
            self.canvas_planche.pieces = self.convertir_case_a_piece()

            self.canvas_planche.dessiner_pieces()

            # determiner si partie terminee et si il y a un gagnant

            if self.partie.partie_terminee():
                self.partie.determiner_gagnant()

                message = messagebox.askyesno('Partie terminee', 'Voulez-vous jouer une nouvelle partie',icon='warning')



                if message == True:
                    self.partie.planche.initialiser_planche_par_default()
                    self.canvas_planche.pieces = self.convertir_case_a_piece()
                    self.canvas_planche.dessiner_pieces()
                else:
                    f.quit()


            self.messages['foreground'] = 'black'




if __name__ == '__main__':
    f = Fenetre()
    f.mainloop()
