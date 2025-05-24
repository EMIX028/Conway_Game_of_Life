from p5 import *
import p5_utils as pm
import jeu as jv
import os
import threading
import numpy
import tkinter as tk
from tkinter import filedialog
import random
from get_res import*
import ctypes
import pygame
import sys
import json


pygame.mixer.init()

MAX_RAM_PERCENTAGE = 0.8
resolutions = get_supported_resolutions()

index_page = "Main_Menu"

res_x, res_y = resolutions[0][0], resolutions[0][1]

nbr_cell, taille_cell = None, None

def calculer_taille_et_nombre_cellules(taille_min=15, taille_max=30):
    max_cellules = 100  # ne pas dépasser
    for taille in range(taille_max, taille_min - 1, -1):
        nb_x = res_x // taille
        nb_y = res_y // taille
        nbr = min(nb_x, nb_y)
        if nbr <= max_cellules:
            return nbr, taille
    return 20, taille_min


nbr_cell, taille_cell = calculer_taille_et_nombre_cellules()


jv.offset_x = round( ( (res_x/2) - (taille_cell*nbr_cell / 2) )* 0.15 , 0 )
jv.offset_y = (res_y/2) - (taille_cell*nbr_cell / 2)

#couleur
Bleu_fonce = (52, 77, 137)
Bleu_clair = (151, 176, 225)
Blanc = (240, 239, 230)
Noir = (21, 28, 44)
Rouge_fonce = (153, 60, 87)
Rouge_clair = (192, 121, 145)

#sons
Sound_BtnClick = pm.Son("ressource/mouse_click.wav",0.5)
Scroll = pm.Son("ressource/step.mp3",1)
sfx = [Sound_BtnClick,Scroll]


# splash screen
show_splash = True


jeu_vie = pm.Fenetre()


def changer_index(index):
    """changer l'index de fenetre pour changer de page"""
    assert type(index) == str,"doit être un str et etre le nom d'une fenetre"
    global index_page,jeu_vie
    jeu_vie.cacher_fenetre(index_page)
    jeu_vie.show(index)
    index_page = index


def fonction_Btn_reset(obj, option=None, liste=None):
    """remet a 0 la grille classique"""
    obj.change_cellules(option,liste)
    if obj.en_jeu:
        obj.toggle_jeu()
        Btn_start.change_text("Start")



def sauvegarder_grille(grille, dossier='save'):
    """sauvegarde la grille dans un fichier txt"""
    chemin_script = os.getcwd()
    chemin_sauvegarde = os.path.join(chemin_script, dossier)
    if not os.path.exists(chemin_sauvegarde):
        os.makedirs(chemin_sauvegarde)
    i = 0
    while True:
        nom_fichier = f"save{i}.txt"
        chemin_fichier = os.path.join(chemin_sauvegarde, nom_fichier)
        if not os.path.exists(chemin_fichier):
            break
        i += 1
    with open(chemin_fichier, 'w') as f:
        for ligne in grille:
            f.write(str(ligne) + '\n')
    print(f"Sauvegarde réalisée dans : {chemin_fichier}")


def importer_fichier():
    """retourne une liste de liste du fichier texte qu'on a selectionné"""
    liste = []
    #fenetre tkinter
    fen = tk.Tk()
    fen.withdraw()
    #explorateur de fichier
    chemin_fichier = filedialog.askopenfilename( title="Choisir un fichier texte", filetypes=[("Fichiers texte", "*.txt")] )
    if not chemin_fichier:
        print("Aucun fichier sélectionné")
        return []
    try:
        with open(chemin_fichier, "r") as f:
            for ligne in f:
                ligne = ligne.strip()
                if ligne:
                    try:
                        ligne_liste = eval(ligne, {"__builtins__": None}, {})
                        if isinstance(ligne_liste, list):
                            liste.append([int(val) for val in ligne_liste])
                        else:
                            print("Ligne ignorée (pas une liste) :", ligne)
                    except Exception as e:
                        print("Erreur lors de l'évaluation de la ligne :", ligne)
                        print("Exception :", e)
    except Exception as e:
        print("Erreur lors de la lecture du fichier :", e)
    return liste



def fonction_Btn_import(obj):
    """fonction qui importe la liste d'état de cellule dans la grille et l'ajuste en fonction de la taille de la grille"""
    try:
        liste_imp = importer_fichier()
        nb_lignes_obj = len(obj.cellules)
        nb_colonnes_obj = len(obj.cellules[0])
        taille_cellule = obj.cellules[0][0].taille
        ajustement = False
        if len(liste_imp) > nb_lignes_obj:
            liste_imp = liste_imp[:nb_lignes_obj]
            ajustement = True

        while len(liste_imp) < nb_lignes_obj:
            nouvelle_ligne = [0] * nb_colonnes_obj
            liste_imp.append(nouvelle_ligne)
            ajustement = True

        for y in range(nb_lignes_obj):
            if len(liste_imp[y]) > nb_colonnes_obj:
                liste_imp[y] = liste_imp[y][:nb_colonnes_obj]
                ajustement = True

            while len(liste_imp[y]) < nb_colonnes_obj:
                liste_imp[y].append(0)
                ajustement = True

        for y in range(nb_lignes_obj):
            for x in range(nb_colonnes_obj):
                if y >= len(obj.cellules):
                    ligne = []
                    for col in range(nb_colonnes_obj):
                        cellule = Cellule(col * taille_cellule, y * taille_cellule, taille_cellule)
                        ligne.append(cellule)
                    obj.cellules.append(ligne)
                    ajustement = True
                elif x >= len(obj.cellules[y]):
                    cellule = Cellule(x * taille_cellule, y * taille_cellule, taille_cellule)
                    obj.cellules[y].append(cellule)
                    ajustement = True
                obj.cellules[y][x].etat = liste_imp[y][x]
        if ajustement:
            print("Le fichier importé a été ajusté (tronqué ou complété) pour correspondre à la taille de la grille")
        else:
            print("Importation réussie sans ajustement")
    except Exception as e:
        print(f"Erreur de format : {e}")


def fonction_Btn_start(obj):
    """ lance le jeu"""
    obj.toggle_jeu()
    if obj.en_jeu:
        Btn_start.change_text("Stop")
    else:
        Btn_start.change_text("Start")

def fonction_btn_param():
    """ fonction qui lance le panel paramètre"""
    P_param.show()
    Btn_Solo.switch_click()
    Btn_param.switch_click()
    Btn_quitter.switch_click()

def fonction_btn_exit():
    """ fonction qui ferme le panel paramètre"""
    P_param.cacher()
    Btn_Solo.switch_click()
    Btn_param.switch_click()
    Btn_quitter.switch_click()


def fonction_gen(k):
    assert type(k) == int,"doit être un int"
    """calcul plusieurs génération à la suite"""
    if k>0:
        for i in range(k) :
            g.etat_suivant()
    else:
        for i in range(abs(k)):
            g.revenir_en_arriere()


def info_cell(obj):
    """renvoie sous forme de tuple toute les informations concernant la grille"""
    nb_cell = obj.nb_cell()
    res = None
    taille_grille = len(obj.cellules)**2
    pr_bleu = round( (nb_cell[0] / taille_grille) * 100 , 2)
    pr_rouge = round( (nb_cell[1] / taille_grille) * 100 , 2)
    if pr_bleu > pr_rouge:
        res = pr_bleu
    else:
        res = pr_rouge
    return nb_cell[0] , pr_bleu , nb_cell[1] , pr_rouge, res


def apply_resolution(res):
    """ applique la résolution a la fenetre ainsi que tout les objets qui ont besoin d'être adapté selon la taille"""
    global res_x, res_y, nbr_cell, taille_cell, g, filtres,LifeTimeG

    res_x, res_y = res
    size(res_x, res_y)
    nbr_cell, taille_cell = calculer_taille_et_nombre_cellules()
    jv.offset_x = round(((res_x / 2) - (taille_cell * nbr_cell / 2)) * 0.15, 0)
    jv.offset_y = (res_y / 2) - (taille_cell * nbr_cell / 2)
    g.nb ,g.taille = nbr_cell,taille_cell
    LifeTimeG.nb ,LifeTimeG.taille = nbr_cell,taille_cell
    for fil in filtres:
        fil.x = res_x
        fil.y = res_y


def ajuster_volume(liste,valeur, direction):
    """modifie le volume pour toute la liste de son"""
    assert type(liste) == list,"doit être une d'objet de type son"
    volume = valeur / 10
    for son in liste:
        son.set_volume(volume)


def choisir_filtre(objet_filtre):
    """active un filtre"""
    global filtre_actif
    for f in filtres:
        f.cacher()

    filtre_actif = objet_filtre
    if filtre_actif:
        filtre_actif.afficher_objet = True
        filtre_actif.niv(0)
        S_filtre.value = 0
    else:
        S_filtre.value = 0


def changer_niveau_filtre(val, direction):
    """changer l'intensité d'un filtre"""
    if filtre_actif:
        filtre_actif.niv(val)


def fonction_Btn_lancer(obj):
    """lance le jeu pour le mode LifeTime"""
    obj.toggle_jeu()
    if obj.en_jeu:
        Btn_lancer.change_text("Stop")
    else:
        Btn_lancer.change_text("Start")

def fonction_btn_restart():
    """remet le jeu à 0 pour la grille du mode LifeTime"""
    T_loose.contenu = f""
    P_loose.cacher()
    LifeTimeG.change_cellules("reset")
    Btn_lancer.click()
    Btn_home1.click()

def fnc_aff_ploose():
    """affiche le panel quand on perd"""
    P_loose.show()
    Btn_lancer.not_click()
    Btn_home1.not_click()



def setup():
    global f, Btn_quitter, splash_image, start_time, Btn_reset, Btn_import, Btn_Bac,Btn_random,resolutions,DD_res,Btn_home, g , Btn_save,T_loose,Btn_home1,Btn_home_expend, mode_expend_actif
    global Btn_param, Btn_start, Btn_prev, Btn_next, Btn_Solo, Btn_lifetime,P_param,Btn_exit, fenetre,S_SFX,LifeTimeG,Btn_lancer,P_loose,Btn_reset_expend,Btn_switchT
    global Btn_gen10,Btn_gen100, Btn_degen10,Btn_degen100,T_titre,T_res,filtre_actif,filtres,S_filtre ,T_Daltonisme,T_niv,T_sons,T_sfx,Btn_Back,Btn_restart,Btn_start_expend,DD_filtre
    size(res_x, res_y)
    title("Jeu de la vie")
    f = create_font("./LiberationSans-Regular.ttf", 15)

    g = jv.Grille(nbr_cell, taille_cell)
    LifeTimeG = jv.Grille(nbr_cell, taille_cell,True)


    #image du splash screen
    splash_image = load_image('splash_image.jpg')
    start_time = millis()

    #filtre
    filtres = [
        pm.Filtre( res_x, res_y , pm.dict_prota,"protanopie"),
        pm.Filtre(res_x, res_y, pm.dict_deutero, name="Deuteranopie"),
        pm.Filtre(res_x, res_y, pm.dict_tritano, name="Tritanopie")
              ]

    filtre_actif = None  # Valeur par défaut


    #boutons
    ## Paramètres
    T_titre = pm.Texte("Paramètres" ,0.5,0.2,48)
    T_res = pm.Texte("Résolutions : ",0.3,0.35,32)
    T_Daltonisme = pm.Texte("Daltonismes :",0.3,0.45,32)
    T_niv = pm.Texte("Niveaux :",0.35,0.53,24)
    T_sons = pm.Texte("Effet Sonores :",0.3,0.65,32)
    T_sfx = pm.Texte("SFX :",0.35,0.72,24)
    Btn_exit = pm.Bouton(x=0.8,y=0.24,rgba= Rouge_fonce,command= lambda : fonction_btn_exit(),size=32,radius=10,text=" X ",fc=Blanc,percent=True,hov=Rouge_clair,sound=Sound_BtnClick)
    DD_res = pm.DropdownMenu(0.5, 0.35, resolutions, on_select=apply_resolution,couleur_fond = Bleu_fonce,hov = Bleu_clair,couleur_font= Blanc,sound = Sound_BtnClick)
    S_SFX = pm.Slider( x=0.5, y=0.72, steps=11, value=5 , knob_color=(180,), knob_act=(100,), on_change=ajuster_volume,percent=True,arg = sfx,son = Scroll)
    S_filtre = pm.Slider(x=0.5, y=0.53,steps=6, value=0,knob_color=(180,),knob_act = (100,),son = Scroll,on_change=changer_niveau_filtre, percent=True)
    DD_filtre = pm.DropdownMenu( x=0.5, y=0.45, options=[None] + filtres, on_select=choisir_filtre, couleur_fond=Bleu_fonce, hov=Bleu_clair, couleur_font=Blanc, sound=Sound_BtnClick)

    P_param = pm.Panel(x=0.5,y=0.5,w=0.7,h=0.7,rgba=(50,50,50,140),liste_obj=[S_SFX,Btn_exit,T_titre,T_res,S_filtre ,T_Daltonisme,T_niv,T_sons,T_sfx,DD_filtre,DD_res])

    ## Main_menu

    Btn_Solo = pm.Bouton(0.5, 0.35, Bleu_fonce, lambda: changer_index("Solo_Menu"), "start", f, Blanc , 5, 45, 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_param = pm.Bouton(0.5, 0.5 ,Bleu_fonce, lambda: fonction_btn_param(), "Paramètre", f, Blanc , 5, 45, 10, (255,255,255,255), 0,True,Bleu_clair,Sound_BtnClick)
    Btn_quitter = pm.Bouton(0.5, 0.65, Rouge_fonce, lambda: exit(), "Quitter", f, Blanc , 5, 45, 10, (255,255,255,255),0,True,Rouge_clair,Sound_BtnClick)


    ## Solo_Menu

    Btn_Bac = pm.Bouton(0.5, 0.45, Bleu_fonce, lambda: changer_index("BaS_Limit"), "Bac à sable", f, Blanc , 5, 45, 10, (255,255,255,255), 0,True,Bleu_clair,Sound_BtnClick)
    Btn_lifetime = pm.Bouton(0.5, 0.6, Bleu_fonce, lambda: changer_index("LifeTime"), "LifeTime", f, Blanc , 5, 45, 10, (255,255,255,255), 0,True,Bleu_clair,Sound_BtnClick)
    Btn_Back = pm.Bouton(0.05, 0.06, Bleu_fonce, lambda: changer_index("Main_Menu"), "Back", f, Blanc , 5, 45, 10, (255,255,255,255), 0,True,Bleu_clair,Sound_BtnClick)


    ## Mode LifeTime
    Btn_lancer = pm.Bouton(0.7 , 0.1,Bleu_fonce,lambda : fonction_Btn_lancer(LifeTimeG) ,"Start", f , Blanc , 5, 45 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_restart = pm.Bouton(0.5,0.7,Bleu_fonce,lambda : fonction_btn_restart() ,"Restart", f , Blanc , 5, 45 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    T_loose = pm.Texte(f"",0.5,0.4,45,None)
    Btn_home1 = pm.Bouton(0.9, 0.1, Rouge_fonce, lambda: changer_index("Main_Menu"), "Home", f, Blanc, 5, 45, 10, (255, 255, 255, 255), 0, True,Rouge_clair,Sound_BtnClick)
    P_loose = pm.Panel(x=0.5,y=0.5,w=0.7,h=0.7,rgba=(50,50,50,140),liste_obj=[Btn_restart,T_loose])


    ## Mode bac a sable

    Btn_prev = pm.Bouton(x=0.72, y=0.1, rgba=Bleu_fonce, command=lambda : g.revenir_en_arriere(), text=" < ", font=f, fc=Blanc, size=45, radius=10, percent = True,hov=Bleu_clair,sound=Sound_BtnClick)
    Btn_next = pm.Bouton(0.92, 0.1, Bleu_fonce, lambda :g.etat_suivant(), " > ", f, Blanc, 5, 45, 10, (255,255,255,255), 0,True,Bleu_clair,Sound_BtnClick)
    Btn_start = pm.Bouton(0.82 , 0.1,Bleu_fonce,lambda : fonction_Btn_start(g) ,"Start", f , Blanc , 5, 45 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_reset = pm.Bouton(0.9,0.75,Bleu_fonce,lambda : fonction_Btn_reset(g,"reset") ,"Reset", f , Blanc , 5, 45 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_save = pm.Bouton(0.75,0.9,Bleu_fonce,lambda : sauvegarder_grille(g.cellules) ,"save", f , Blanc , 5, 45 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_import = pm.Bouton(0.9,0.9,Bleu_fonce,lambda : fonction_Btn_import(g) ,"Import", f , Blanc , 5, 45 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_random = pm.Bouton(0.75,0.75,Bleu_fonce,lambda : g.change_cellules("random") ,"Random", f , Blanc , 5, 45 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_home = pm.Bouton(0.9, 0.65, Rouge_fonce, lambda: changer_index("Main_Menu"), "Home", f, Blanc, 5, 45, 10, (255, 255, 255, 255), 0, True,Rouge_clair,Sound_BtnClick)
    Btn_gen10 = pm.Bouton(0.87 , 0.2,Bleu_fonce,lambda : fonction_gen(10) ,"+10", f , Blanc , 5, 30 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_gen100 = pm.Bouton(0.94 , 0.2,Bleu_fonce,lambda : fonction_gen(100) ,"+100", f , Blanc , 5, 30 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_degen100 = pm.Bouton(0.7 , 0.2,Bleu_fonce,lambda : fonction_gen(-100) ,"-100", f , Blanc , 5, 30 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_degen10 = pm.Bouton(0.77 , 0.2,Bleu_fonce,lambda : fonction_gen(-10) ,"-10", f , Blanc , 5, 30 , 10, (255,255,255,255),0,True,Bleu_clair,Sound_BtnClick)
    Btn_switchT = pm.Bouton(0.75, 0.65, Bleu_fonce, lambda: g.switch(), "Switch", f, Blanc, 5, 45, 10, (255, 255, 255, 255), 0, True,Bleu_clair,Sound_BtnClick)

    ## fenetres

    jeu_vie.ajouter_fenetre("Main_Menu",[Btn_Solo,Btn_param,Btn_quitter,P_param])
    jeu_vie.ajouter_fenetre("Solo_Menu",[Btn_Bac,Btn_lifetime,Btn_Back])
    jeu_vie.ajouter_fenetre("BaS_Limit",[Btn_prev,Btn_switchT,Btn_next,Btn_start,Btn_reset,Btn_import,Btn_save,Btn_random,g,Btn_home,Btn_gen10,Btn_gen100,Btn_degen10,Btn_degen100])
    jeu_vie.ajouter_fenetre("LifeTime",[LifeTimeG,Btn_lancer,P_loose,Btn_home1])


def draw():
    global splash_image , show_splash
    size(res_x , res_y)
    if show_splash:
        background(*Noir)
        image(splash_image, 0, 0, res_x, res_y)
        if millis() - start_time > 3000:
            show_splash = False
    else:
        # param Fenêtre
        background(*Noir)
        text_font(f)
        stroke(0)

        jeu_vie.afficher_fenetres(index_page)


        if index_page == "BaS_Limit":
            ## mode classique
            T_nbr_gen = pm.Texte(("nbr de gen : " + str(len(g.historique))),0.8,0.4,48)
            T_etat = pm.Texte("état : ",0.73,0.5,48)
            state = pm.Rectangle(x=0.8,y=0.51,w=0.05,h=0.07,rgba=(180,0,0,255))
            T_nb = pm.Texte(f" bleues : { info_cell(g)[0] } ( { info_cell(g)[1] }%) , Rouges : { info_cell(g)[2] } ({ info_cell(g)[3] }%)",0.8 , 0.3,24)

            T_nbr_gen.afficher()
            T_nb.afficher()
            T_etat.afficher()

            if g.en_jeu:
                g.etat_suivant()
                state.rgba = (0,180,0,255)
            else:
                state.rgba = (180,0,0,255)
            state.afficher()


        if index_page == "LifeTime":
            ## Mode LifeTime
            T_score = pm.Texte(f"Scores : {len(LifeTimeG.historique)}",0.8,0.4,48)
            T_score.afficher()
            T_expli = pm.Texte("Le but du jeu est de faire\nsurvivre les cellules\nles plus longtemps possible\n(oscilateur et forme inerte\nnon compté)",0.8,0.7,30)
            T_expli.afficher()

            if LifeTimeG.mode_survie:
                if LifeTimeG.en_jeu:
                    LifeTimeG.etat_suivant()


                    # Vérifie fin de partie : extinction
                    nb_bleues, nb_rouges = LifeTimeG.nb_cell()
                    if nb_bleues == 0 and nb_rouges == 0:
                        T_loose.contenu = f"Perdu ! Toutes les cellules sont mortes.\n\n\n\n                        scores : {len(LifeTimeG.historique)}"
                        fnc_aff_ploose()
                        LifeTimeG.en_jeu = False
                        Btn_lancer.change_text("Start")

                    # Vérifie inactivité (motif fixe)
                    elif len(LifeTimeG.historique) > 1:
                        if LifeTimeG.historique[-1] == LifeTimeG.historique[-2]:
                            T_loose.contenu = f"Perdu ! Toute les cellules sont inactives.\n\n\n\n                        scores : {len(LifeTimeG.historique)}"
                            fnc_aff_ploose()
                            LifeTimeG.en_jeu = False
                            Btn_lancer.change_text("Start")

                    # Vérifie oscillation
                    for i in range(len(LifeTimeG.historique) - 2):
                        if LifeTimeG.historique[-1] == LifeTimeG.historique[i]:
                            periode = len(LifeTimeG.historique) - i - 1
                            T_loose.contenu = f"Perdu ! Motif oscillant détecté de période {periode}.\n\n\n\n                        scores : {len(LifeTimeG.historique)}"
                            fnc_aff_ploose()
                            LifeTimeG.en_jeu = False
                            Btn_lancer.change_text("Start")

    for fil in filtres:
        if fil.niveau > 0:
            fil.afficher()


def mouse_pressed(event):
    jeu_vie.verif(event,event.x,event.y)

def mouse_released(event):
    jeu_vie.mouse_released(event)

def mouse_dragged(event):
    jeu_vie.mouse_dragged(event)

def mouse_moved(event):
    jeu_vie.mouse_moved(event)

def mouse_wheel(event):
    jeu_vie.mouse_wheel(event)

def key_pressed():
    if key == " ":
        fonction_Btn_start(g)


def lancer_jeu():
    threading.Thread(target=lambda: run(frame_rate=30)).start()

lancer_jeu()

