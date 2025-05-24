import numpy
from p5 import *
import threading
import random
from collections import defaultdict
import math

offset_x = 0
offset_y = 0  # marge pour le jeu

class Cellule:
    def __init__(self, x, y, taille, etat=0):
        """
        x : position x de la cellule, int
        y : position y de la cellule, int
        taille: taille de la cellule sur la fenetre, int

        Les états de la cellule : 0 (morte), 1 (bleue), 2 (rouge)
        """
        assert type(x) == int, "doit être un int"
        assert type(y) == int, "doit être un int"
        assert type(taille) == int, "doit être un int"

        self.x = x
        self.y = y
        self.taille = taille
        self.etat = etat

    def __repr__(self):
        return str(self.etat)

    def afficher(self):
        """Affiche la cellule à l'écran en fonction de son état"""
        stroke(255)
        if self.etat == 0:
            fill(200)  # Cellule morte
        elif self.etat == 1:
            fill(151, 176, 225)  # Cellule bleue
        elif self.etat == 2:
            fill(192, 121, 145)  # Cellule rouge
        rect(self.x + offset_x, self.y + offset_y, self.taille, self.taille)

    def changer_etat(self):
        """Change l'état de la cellule (cycle : morte -> bleue -> rouge -> morte)."""
        self.etat = (self.etat + 1) % 3


class Grille:
    """Gère la grille entière avec toute les cellules"""
    def __init__(self, nb_cellules, taille_cellule,mode_survie=False):
        """
        nb_cellules : nombre de cellule dans la grille, int
        taille_cellule : donne la taille pour toute les cellules pour pas avoir e problème d'affichage, int
        """

        assert type(nb_cellules) == int,"doit être int"
        assert type(taille_cellule) == int,"doit être int"

        self.nb = nb_cellules
        self.taille = taille_cellule
        self.cellules = [[Cellule(x * taille_cellule, y * taille_cellule, taille_cellule) for x in range(nb_cellules)] for y in range(nb_cellules)]
        self.en_jeu = False
        self.historique = []
        self.creer = False
        self.afficher_objet = True
        self.mode_survie = mode_survie

    def nb_cell(self):
        bleu = 0
        rouge = 0
        for ligne in self.cellules:
            for cellule in ligne:
                if cellule.etat == 1:
                    bleu += 1
                elif cellule.etat == 2:
                    rouge += 1
        return bleu,rouge


    def __repr__(self):
        res = f""
        for k in range(self.nb):
            res = res + f"{self.cellules[k]} \n"
        return res


    def sauvegarder_etat(self):
        som = 0
        for liste in self.cellules:
            dupli = [cell.etat for cell in liste]
            som = som + sum(dupli)
        if som > 0:
            copie = [[cell.etat for cell in ligne] for ligne in self.cellules]
            self.historique.append(copie)
        if len(self.historique) > 1:
            if self.historique[-1] == self.historique[-2]:
                print("inactif")
                self.toggle_jeu()


    def revenir_en_arriere(self):
        if self.historique:
            dernier = self.historique.pop()
            for y in range(self.nb):
                for x in range(self.nb):
                    self.cellules[y][x].etat = dernier[y][x]


    def change_cellules(self, option, liste=None):
        assert type(option) == str,"doit être un str qui est affecté a une option (reset,random)"
        if option == "reset":
            self.cellules = [[Cellule(x * self.taille, y * self.taille, self.taille) for x in range(self.nb)] for y in range(self.nb)]
            self.historique = []
        elif option == "random":
            self.historique = []
            for ligne in self.cellules:
                for cellule in ligne:
                    cellule.etat = random.choice([0,1,2])
        elif liste is not None:
            self.cellules = liste
            self.historique = []


    def afficher(self):
        """Affiche les lignes de la grille et les cellules vivantes uniquement"""
        if self.afficher_objet:
            self.creer = True
            stroke(255,)
            stroke_weight(2)
            for i in range(self.nb + 1):
                x = i * self.taille + offset_x
                y = i * self.taille + offset_y
                line(offset_x, y, offset_x + self.nb * self.taille, y)  # lignes horizontales
                line(x, offset_y, x, offset_y + self.nb * self.taille)  # lignes verticales
            # Affiche uniquement les cellules vivantes
            for ligne in self.cellules:
                for cellule in ligne:
                    if cellule.etat != 0:
                        cellule.afficher()


    def changer_cellule_sous_souris(self, mx, my):
        """
        Change l'état de la cellule quand on clique avec la souris
        mx : position x de la souris
        my : position y de la souris
        """
        if self.afficher_objet and self.creer:
            col = int((mx - offset_x) / self.taille)
            lig = int((my - offset_y) / self.taille)
            if 0 <= lig < self.nb and 0 <= col < self.nb:
                self.cellules[lig][col].changer_etat()


    def maj_etat_bleu(self, x, y, copie):
        """
        Met à jour l'état de la cellule (x, y) si elle est bleue :
        - Survie : 2 ou 3 voisins bleus et moins de 5 rouges
        - Naissance : si cellule morte et 3 voisins bleus
        - Interaction :
            - Si 4 voisins rouges ou plus, la cellule bleue meurt (domination rouge)
        """
        cellule = self.cellules[y][x]
        bleus = 0
        rouges = 0
        voisins = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1), (1, 0),  (1, 1)]

        for dy, dx in voisins:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.nb and 0 <= nx < self.nb:
                etat = copie[ny][nx]
                if etat == 1:
                    bleus += 1
                elif etat == 2:
                    rouges += 1

        if cellule.etat == 1:
            if rouges >= 4:
                cellule.etat = 0  # tuée par la dominance rouge
            elif bleus in (2, 3) and rouges < 5:
                cellule.etat = 1  # survie
            else:
                cellule.etat = 0  # mort
        elif cellule.etat == 0:
            if bleus == 3:
                cellule.etat = 1  # naissance


    def maj_etat_rouge(self, x, y, copie):
        """
        Met à jour l'état de la cellule (x, y) si elle est rouge, selon HighLife :
        - Survie : 2 ou 3 voisins rouges
        - Naissance : si cellule morte et 3 ou 6 voisins rouges
        - Interaction :
            - Si 4 voisins bleus ou plus, la cellule rouge meurt (domination bleue)
        """
        cellule = self.cellules[y][x]
        rouges = 0
        bleus = 0
        voisins = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1), (1, 0),  (1, 1)]

        for dy, dx in voisins:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.nb and 0 <= nx < self.nb:
                etat = copie[ny][nx]
                if etat == 2:
                    rouges += 1
                elif etat == 1:
                    bleus += 1

        if cellule.etat == 2:
            if bleus >= 4:
                cellule.etat = 0  # tuée par la dominance bleue
            elif rouges in (2, 3):
                cellule.etat = 2  # survie
            else:
                cellule.etat = 0  # mort
        elif cellule.etat == 0:
            if rouges in (3, 6):
                cellule.etat = 2  # naissance




    def etat_suivant(self):
        """
        Applique les règles d'évolution à toute la grille, séparément pour les bleus et les rouges.
        """
        self.sauvegarder_etat()  # save avant de changer l’état
        copie = [[c.etat for c in ligne] for ligne in self.cellules]

        for y in range(self.nb):
            for x in range(self.nb):
                self.maj_etat_bleu(x, y, copie)
        for y in range(self.nb):
            for x in range(self.nb):
                self.maj_etat_rouge(x, y, copie)


    def toggle_jeu(self):
        """Active ou désactive l'exécution automatique du jeu."""
        self.en_jeu = not self.en_jeu


    def cacher(self):
        """cache la grille"""
        self.en_jeu = False
        self.historique = []
        self.afficher_objet = False

    def show(self):
        """affiche la grille"""
        self.change_cellules("reset")
        self.afficher_objet = True

    def superficie_cellules(self):
        """
        Calcule la superficie totale des cellules bleues et rouges.

        Retourne:
            tuple: (superficie_bleue, superficie_rouge)
        """
        superficie_bleue = 0
        superficie_rouge = 0

        for ligne in self.cellules:
            for cellule in ligne:
                if cellule.etat == 1:  # Cellule bleue
                    superficie_bleue += cellule.taille ** 2
                elif cellule.etat == 2:  # Cellule rouge
                    superficie_rouge += cellule.taille ** 2

        return superficie_bleue, superficie_rouge

    def switch(self):
        """rend les cellule bleus rouge et inversemment"""
        for ligne in self.cellules:
            for cellule in ligne:
                if cellule.etat == 1:
                    cellule.etat = 2
                elif cellule.etat ==2:
                    cellule.etat = 1


