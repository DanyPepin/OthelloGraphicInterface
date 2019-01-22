class PartieTerminee(Exception):

    def partiee_terminee(self):

    try:
    piece = self.canvas_planche.pieces[position_message]

    # On change la valeur de l'attribut position_selectionnee.

    self.position_selectionnee = position_message

    # self.messages['text'] = 'Pièce sélectionnée : {} à la position {}.'.format(piece, self.position_selectionnee)


    except KeyError:

    if self.partie.partie_terminee():
        message = 'Partie terminee'
            # message box ici

            # reinitialisation
        self.partie.planche.initialiser_planche_par_default()
        self.canvas_planche.pieces = self.convertir_case_a_piece()
        self.canvas_planche.dessiner_pieces()
        # print(self.canvas_planche.pieces)

    self.messages['foreground'] = 'black'
    self.messages['text'] = message
