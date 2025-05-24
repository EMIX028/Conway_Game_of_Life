from p5 import *
import pygame



class Son:
    def __init__(self, chemin_fichier, volume=1.0):
        """chemin_fichier : chemin vers le fichier son
            volume : puissance du son (attention a la saturation)
        """
        assert type(chemin_fichier) == str,"doit être un chemin de fichier en str"
        assert type(volume) == int or type(volume) == float,"doit être une valeur int ou float"
        self.son = pygame.mixer.Sound(chemin_fichier)
        self.son.set_volume(volume)
        self.channel = None  ## Pour suivre sur quel canal le son joue

    def jouer(self, boucle=False):
        loops = -1 if boucle else 0
        self.channel = self.son.play(loops=loops)

    def set_volume(self, volume):
        assert type(volume) == int or type(volume) == float,"doit être une valeur int ou float"
        self.volume = volume
        self.son.set_volume(volume)

    def arreter(self):
        if self.channel is not None:
            self.channel.stop()


class Rectangle:
    def __init__(self, x=0.5, y=0.5, w=0.2, h=0.1, rgba=(255, 255, 255, 255), oc=(0, 0, 0, 255), ot=0):
        """Crée un rectangle
            x : position x, float ; int
            y : position y, float ; int
            w : largeur du rectangle, float ; int
            h : hauteur du rectangle; float ; int
            rgba : couleur rgba du rectangle, tuples d'éléments inférieur ou égal à 255
            oc : couleur de la bordure du rectangle, tuples d'éléments inférieur ou égal à 255
            ot : epaisseur de la bordure, int
        """
        assert type(x) == float or type(x) == int,"doit être float"
        assert type(y) == float or type(y) == int,"doit être float"
        assert type(w) == float or type(w) == int,"doit être float"
        assert type(h) == float or type(h) == int,"doit être float"
        assert type(rgba) == tuple,"doit être un tuple"
        for nbr in rgba:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(oc) == tuple,"doit être un tuple"
        for nbr in oc:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(ot) == int,"doit être un nombre int"
        self.x = x
        self.y = y
        self.w_percent = w
        self.h_percent = h
        self.rgba = rgba
        self.oc = oc
        self.ot = ot
        self.afficher_objet = True
        self.en_animation = False
        self.animation_type = None  ## "hori" ou "verti"
        self.direction = "centre"
        self.frame_step = 1
        self.animation_mode = "in"  ## "in" apparition ou "out" disparition
        self.current_w = 0
        self.current_h = 0

    def afficher(self):
        """dessine le rectangle"""
        if self.afficher_objet:
            x_pix = self.x * width
            y_pix = self.y * height
            w_pix = self.w_percent * width
            h_pix = self.h_percent * height
            w_aff = self.current_w if self.en_animation else w_pix
            h_aff = self.current_h if self.en_animation else h_pix

            if self.animation_type == "hori":
                if self.direction == "gauche":
                    x_aff = x_pix - w_aff
                elif self.direction == "droite":
                    x_aff = x_pix
                else:
                    x_aff = x_pix - w_aff / 2
                y_aff = y_pix - h_pix / 2
            elif self.animation_type == "verti":
                if self.direction == "haut":
                    y_aff = y_pix - h_aff
                elif self.direction == "bas":
                    y_aff = y_pix
                else:
                    y_aff = y_pix - h_aff / 2
                x_aff = x_pix - w_pix / 2
            else:
                x_aff = x_pix - w_pix / 2
                y_aff = y_pix - h_pix / 2
            if self.ot > 0:
                stroke(*self.oc)
                stroke_weight(self.ot)
            else:
                no_stroke()
            fill(*self.rgba)
            rect(x_aff, y_aff, w_aff, h_aff)

    def cacher(self):
        """cache le rectangle"""
        self.afficher_objet = False

    def show(self):
        """affiche le rectangle"""
        self.afficher_objet = True

    def switch(self):
        """switch afficher/cacher"""
        self.afficher_objet = not self.afficher_objet

    def lancer_animation(self, option="hori", frame=2, direction="centre"):
        """lance une animation d'apparition"""
        self.afficher_objet = True
        self.en_animation = True
        self.animation_type = option
        self.direction = direction
        self.frame_step = frame
        self.animation_mode = "in"
        if option == "hori":
            self.current_w = 0
            self.current_h = self.h_percent * height
        elif option == "verti":
            self.current_h = 0
            self.current_w = self.w_percent * width

    def lancer_disparition(self, option="hori", frame=2, direction="centre"):
        """lance une animation de disparition"""
        self.afficher_objet = True
        self.en_animation = True
        self.animation_type = option
        self.direction = direction
        self.frame_step = frame
        self.animation_mode = "out"
        if option == "hori":
            self.current_w = self.w_percent * width
            self.current_h = self.h_percent * height
        elif option == "verti":
            self.current_h = self.h_percent * height
            self.current_w = self.w_percent * width

    def update_animation(self):
        """met a jour l'animation dans la fenetre"""
        if self.en_animation:
            if self.animation_type == "hori":
                target = self.w_percent * width
                if self.animation_mode == "in":
                    self.current_w += self.frame_step
                    if self.current_w >= target:
                        self.current_w = target
                        self.en_animation = False
                else:  ## disparition
                    self.current_w -= self.frame_step
                    if self.current_w <= 0:
                        self.current_w = 0
                        self.en_animation = False
                        self.afficher_objet = False

            elif self.animation_type == "verti":
                target = self.h_percent * height
                if self.animation_mode == "in":
                    self.current_h += self.frame_step
                    if self.current_h >= target:
                        self.current_h = target
                        self.en_animation = False
                else:  ## disparition
                    self.current_h -= self.frame_step
                    if self.current_h <= 0:
                        self.current_h = 0
                        self.en_animation = False
                        self.afficher_objet = False


class Texte:
    def __init__(self, contenu, x=0.5, y=0.5, font_size=16, font=None, rgba=(255,), align_x=CENTER, align_y=CENTER):
        """crée un texte
            contenu : texte
            x : position x
            y : position y
            font_size : taille de police
            font : police
            rgba : couleur de texte
            align_x : justifier en x
            align_y : justifier en y
        """
        assert type(contenu) == str,"doit être une chaine de caractère"
        assert type(x) == float or type(x) == int,"doit être float ou int"
        assert type(y) == float or type(y) == int,"doit être float ou int"
        assert type(font_size) == int,"doit être un int"
        assert type(rgba) == tuple,"doit être un tuple"
        for nbr in rgba:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        self.contenu = contenu
        self.x = x
        self.y = y
        self.font_size = font_size
        self.font = font
        self.align_x = align_x
        self.align_y = align_y
        self.afficher_objet = True
        self.couleur = rgba

    def afficher(self):
        """dessine le texte"""
        if self.afficher_objet:
            x = self.x * width
            y = self.y * height

            push_style()
            fill(*self.couleur)
            text_size(self.font_size)
            if self.font is not None:
                text_font(self.font)
            text_align(self.align_x, self.align_y)
            text(self.contenu, (x, y))
            pop_style()

    def set_texte(self, nouveau_texte):
        """change le texte"""
        self.contenu = nouveau_texte

    def cacher(self):
        """cache le texte"""
        self.afficher_objet = False

    def set_position(self, x, y):
        """change la position du texte"""
        self.x = x
        self.y = y

    def set_font_size(self, font_size):
        """change la taille du texte"""
        self.font_size = font_size

    def set_couleur(self, couleur):
        """change la couleur du texte"""
        self.couleur = couleur



class Bouton:
    def __init__(self, x=0, y=0, rgba=(255,255,255,255), command=None, text="...", font=None, fc=(0,0,0,255), margin=5.0, size=15, radius=0, oc=(0,0,0,255), ot=1, percent=False, hov=None, sound=None):

        """
        Crée un objet Bouton qui effectue une action quand on clique dessus
        x : position x (int / float)
        y : position y (int / float)
        rgba : couleur rgba (255,255,255,255) tuple
        command : fonction
        text : str
        font : police d'écriture
        margin : float
        size : float
        radius : float arrondi du rectangle
        oc : couleur rgba du contour du bouton tuple (255,255,255,255)
        ot : epaisseur de ce contour, int
        hov : couleur quand la souris survole le bouton, tuple de couleur rgba
        sound : son quand on clique sur le bouton, objet de classe Son
        """

        assert type(x) in (int, float), "doit être un int ou float"
        assert type(y) in (int, float), "doit être un int ou float"
        assert type(rgba) == tuple, "doit être un tuple"
        for nbr in rgba:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(text) == str, "doit être un str"
        assert type(margin) in (float, int), "doit être un float ou int"
        assert type(size) == int, "doit être un int"
        assert type(radius) in (int, float), "doit être un int ou float"
        assert type(oc) == tuple and len(oc) == 4, "doit être un tuple de 4 éléments"
        assert type(ot) == int, "doit être un int"
        assert type(percent) == bool, "doit être un bool"
        assert type(hov) == tuple,"doit être un tuple"
        for nbr in hov:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(sound) == Son,"doit être de la classe son"

        self.x = x
        self.y = y
        self.percent = percent
        self.rgba = rgba
        self.command = command
        self.text = text
        self.font = font
        self.fc = fc
        self.margin = margin
        self.size = size
        self.radius = radius
        self.oc = oc
        self.ot = ot
        self.afficher_objet = True
        self.is_click = True

        self.hov = hov if hov else rgba
        self.sound = sound

    def __repr__(self):
        return f"Bouton à la position ({self.x}, {self.y})"

    def _dessiner_arrondi(self, x, y, largeur, hauteur, radius):
        """dessine l'arrondi du bord des boutons"""
        rect((x + radius, y), largeur - 2 * radius, hauteur)
        rect((x, y + radius), largeur, hauteur - 2 * radius)
        ellipse((x + radius, y + radius), radius * 2, radius * 2)
        ellipse((x + largeur - radius, y + radius), radius * 2, radius * 2)
        ellipse((x + radius, y + hauteur - radius), radius * 2, radius * 2)
        ellipse((x + largeur - radius, y + hauteur - radius), radius * 2, radius * 2)

    def rect_arrondi(self, x, y, largeur, hauteur, radius, couleur_remplissage, oc=None, epaisseur=2):
        """dessine entièrement le rectangle arrondis"""
        if oc:
            fill(*oc)
            no_stroke()
            self._dessiner_arrondi(x - epaisseur, y - epaisseur, largeur + epaisseur * 2, hauteur + epaisseur * 2, radius + epaisseur)
        fill(*couleur_remplissage)
        no_stroke()
        self._dessiner_arrondi(x, y, largeur, hauteur, radius)

    def afficher(self):
        """affiche tous le bouton avec rectangle detection pour le clic"""
        if self.afficher_objet:
            text_size(self.size)
            largeur_text = text_width(self.text)
            hauteur_text = self.size + 10
            largeur_bouton = largeur_text + self.margin * 2
            hauteur_bouton = hauteur_text + self.margin * 2

            px = self.x * width if self.percent else width // 2 + self.x
            py = self.y * height if self.percent else height // 2 + self.y

            x_affiche = px - largeur_bouton // 2
            y_affiche = py - hauteur_bouton // 2
            self.hitbox = (x_affiche, y_affiche, largeur_bouton, hauteur_bouton)
            radius_adapte = min(self.radius, largeur_bouton / 2, hauteur_bouton / 2)

        ## Détection du survol souris
        mx, my = mouse_x, mouse_y
        survol = x_affiche <= mx <= x_affiche + largeur_bouton and y_affiche <= my <= y_affiche + hauteur_bouton
        couleur = self.hov if survol and self.is_click else self.rgba

        self.rect_arrondi(x_affiche, y_affiche, largeur_bouton, hauteur_bouton, radius_adapte, couleur, oc=self.oc, epaisseur=self.ot)
        fill(*self.fc)
        text(self.text, (x_affiche + self.margin, y_affiche + self.margin))

    def verifier_clic(self, event):
        """vérifie quand on clic sur le bouton"""
        if self.is_click and self.afficher_objet and hasattr(self, "hitbox"):
            x, y, w, h = self.hitbox
            if x <= event.x <= x + w and y <= event.y <= y + h:
                if self.sound:
                    self.sound.jouer()
                if self.command:
                    self.command()


    def switch(self):
        """de afficher/cacher"""
        self.afficher_objet = not self.afficher_objet

    def cacher(self):
        """cache le bouton"""
        self.afficher_objet = False

    def show(self):
        """affiche le bouton"""
        self.afficher_objet = True

    def not_click(self):
        """empêche le clic"""
        self.is_click = False

    def click(self):
        """remet le clic"""
        self.is_click = True

    def switch_click(self):
        """switch clic/not_clic"""
        self.is_click = not self.is_click

    def change_pos(self, x, y):
        """change la position du bouton"""
        self.x = x
        self.y = y

    def change_text(self, text):
        """change le texte du bouton"""
        self.text = text




class Slider:
    def __init__(self, x, y, length=200, steps=5, value=0, radius=10, line_color=(150,), knob_color=(255,), knob_act=(200, 100, 255), on_change=None, percent=False, son=None,arg=None):
        """
        Crée un objet slider et ça poignet a laquelle on affecte une fonction qui a une valeur différente selon
        qu'on déplace la poignet
        x : position x (int / float)
        y : position y (int / float)
        length : longueur de la barre du slider, int
        steps : nombre d'étape que peut faire la poignet, int
        value : valeur par défaut de la poignet, int
        radius : rayon de la poignet,int
        line_color : couleur rgba de la barre, tuple
        knob_color : couleur rgba de la poignet, tuple
        knob_act : couleur rgba quand on maintient le clique sur la poignet, tuple
        on_change : fonction appliqué au slider
        percent : si on prend une position x,y absolu ou relative à la taille de la fenetre, Boolean
        son : son appliqué quand on déplace la poignet du slider, objet de classe Son
        arg : argument suplémentaire applicable à la fonction
        """
        assert type(x) in (int, float), "doit être un int ou float"
        assert type(y) in (int, float), "doit être un int ou float"
        assert type(length) == int, "doit être un int"
        assert type(steps) == int, "doit être un int"
        assert type(value) == int, "doit être un int"
        assert type(radius) == int, "doit être un int"
        assert type(line_color) == tuple, "doit être un tuple"
        for nbr in line_color:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(knob_color) == tuple, "doit être un tuple"
        for nbr in knob_color:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(knob_act) == tuple, "doit être un tuple"
        for nbr in knob_act:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(percent) == bool, "doit être un bool"
        assert type(son) == Son,"doit être de la classe son"

        self.x = x
        self.y = y
        self.length = length
        self.steps = steps
        self.value = value
        self.radius = radius
        self.line_color = line_color
        self.knob_color = knob_color
        self.knob_act = knob_act
        self.on_change = on_change
        self.dragging = False
        self.step_width = length / (steps - 1)
        self.percent = percent
        self.afficher_objet = True
        self.son = son
        self.arg = arg

    def get_absolute_pos(self):
        if self.percent:
            px = self.x * width
            py = self.y * height
        else:
            px = width // 2 + self.x
            py = height // 2 + self.y
        return px, py

    def afficher(self):
        """dessine le slider sur la fenetre"""
        if self.afficher_objet:
            px, py = self.get_absolute_pos()

            stroke(*self.line_color)
            stroke_weight(4)
            line((px - self.length // 2, py), (px + self.length // 2, py))

            knob_x = px - self.length // 2 + self.value * self.step_width
            no_stroke()

            ## Choix de couleur selon l'état
            if self.dragging:
                fill(*self.knob_act)
            else:
                fill(*self.knob_color)

            circle((knob_x, py), self.radius * 2)

    def verifier_clic(self, event):
        """ vérifie quand on clique sur toute la zone ou est le slider"""
        if self.afficher_objet:
            px, py = self.get_absolute_pos()
            knob_x = px - self.length // 2 + self.value * self.step_width
            if dist((event.x, event.y), (knob_x, py)) <= self.radius + 5:
                self.dragging = True

    def mouse_released(self, event):
        """ vérifie quand on relache le clique de la souris"""
        if self.afficher_objet:
            self.dragging = False

    def mouse_dragged(self, event):
        """vérifie quand on maintient le clique de la souris"""
        if self.afficher_objet and self.dragging:
            px, py = self.get_absolute_pos()
            rel_x = event.x - (px - self.length // 2)
            step = round(rel_x / self.step_width)
            step = max(0, min(self.steps - 1, step))
            if step != self.value:
                direction = 1 if step > self.value else -1
                self.value = step
                if self.on_change:
                    if self.arg is not None:
                        self.on_change(self.arg,self.value, direction)
                    else:
                        self.on_change(self.value, direction)
                if self.son:
                    self.son.jouer()

    def get_value(self):
        """ retourne la valeur actuel du slider"""
        return self.value

    def cacher(self):
        """cache le slider de la fenetre"""
        self.afficher_objet = False




class Filtre:
    def __init__(self,x , y , dictio, name="None"):
        """
        Crée un filtre qui sera positionné sur fenêtre
        x : position x du coin inférieur droit (int)
        y: position y du coin inférieur droit (int)
        name : nom du filtre (str)
        dict: dictionnaire des valeurs du filtre (dict)
        """
        assert type(x) == int,"doit être un int"
        assert type(y) == int, "doit être un int"
        assert type(name) == str,"doit être un str"
        assert type(dictio) == dict,"doit être un dict dictionnaire"
        self.x = x
        self.y = y
        self.name = name
        self.dict = dictio
        self.afficher_objet = True
        self.niveau = 0

    def __repr__(self): return str(self.name)

    def afficher(self):
        """dessine le filtre sur la fenêtre"""
        if self.afficher_objet:
            fill(*self.dict[self.niveau])
            rect(0 , 0 , self.x , self.y)

    def cacher(self):
        self.afficher_objet = False

    def niv(self,val = 0):
        self.niveau = max(0, min(val, len(self.dict)-1))



dict_prota = {
                 0 : (0, 0  , 0  , 0 ),
                 1 : (0, 255, 255, 16),
                 2 : (0, 255, 255, 32),
                 3 : (0, 255, 255, 48),
                 4 : (0, 255, 255, 64),
                 5 : (0, 255, 255, 96)
            }

dict_deutero = {
                 0: (0, 0  , 0  , 0  ),
                 1: (0, 255, 0  , 16 ),
                 2: (0, 255, 0  , 32 ),
                 3: (0, 255, 0  , 48 ),
                 4: (0, 255, 0  , 64 ),
                 5: (0, 255, 0  , 96 )
            }

dict_tritano = {
                 0: (0, 0  , 0  , 0  ),
                 1: (0, 0  , 255, 16 ),
                 2: (0, 0  , 255, 32 ),
                 3: (0, 0  , 255, 48 ),
                 4: (0, 0  , 255, 64 ),
                 5: (0, 0  , 255, 96 )
            }


class DropdownMenu:
    def __init__(self, x=0.5, y=0.5, options=[], default_index=0, w=0.2, h=0.05, font_size=16, max_visible=5, on_select=None,couleur_fond=(220,), hov=(180,),couleur_font=(0,) , sound=None):
        """
        Crée un objet Menu déroulant qui effectue une action quand on clique sur une option du menu
        x : position x (int / float)
        y : position y (int / float)
        options : liste des options qui seront possible de choisir,list
        default_index : paramètre par defaut du menu, int
        w : largeur du menu déroulant, int / float
        h : hauteur du menu déroulant, int / float
        font_size : taille du texte, int
        max_visible : nombre max de choix qui sont visible avant de devoir scroller, int
        on_select : fonction qui s'applique quand on choisis une valeur
        couleur_fond : couleur rgba (255,255,255,255), tuple
        hov : couleur rgba quand on survole un choix avec sa souris (255,255,255,255), tuple
        couleur_font : couleur rgba du texte (255,255,255,255) tuple
        sound : son quand on clique sur le bouton, objet de classe Son
        """
        assert type(x) in (int, float), "doit être un int ou float"
        assert type(y) in (int, float), "doit être un int ou float"
        assert type(w) in (int, float), "doit être un int ou float"
        assert type(h) in (int, float), "doit être un int ou float"
        assert type(options) == list, "doit être une liste"
        assert type(default_index) == int, "doit être un int"
        assert type(font_size) == int,"doit être un int"
        assert type(max_visible) == int,"doit être un int"
        assert type(couleur_fond) == tuple, "doit être un tuple"
        for nbr in couleur_fond:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(hov) == tuple,"doit être un tuple"
        for nbr in hov:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(couleur_font) == tuple, "doit être un tuple"
        for nbr in couleur_font:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        assert type(sound) == Son,"doit être de la classe son"
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.options = options
        self.labels = [str(opt) for opt in options]
        self.selected_index = default_index
        self.font_size = font_size
        self.is_open = False
        self.hover_index = -1
        self.scroll_offset = 0
        self.max_visible = max_visible
        self.on_select = on_select
        self.couleur_fond = couleur_fond
        self.hov = hov
        self.couleur_font = couleur_font
        self.afficher_objet = True
        self.sound = sound

    def afficher(self):
        """dessine tout les éléments du menu déroulant"""
        if self.afficher_objet:
            w = self.w * width
            h = self.h * height
            x = self.x * width - w / 2
            y = self.y * height - h / 2

            push_style()
            fill(*self.couleur_fond)
            rect((x, y), w, h)
            fill(*self.couleur_font)
            text_size(self.font_size)
            text_align(LEFT, CENTER)
            text(self.labels[self.selected_index], (x + 10, y + h / 2))
            triangle( (x + w - 20, y + h / 2 - 5) , (x + w - 10, y + h / 2 - 5) , (x + w - 15, y + h / 2 + 5) )

            if self.is_open:
                visible_options = self.labels[self.scroll_offset:self.scroll_offset + self.max_visible]
                for i, label in enumerate(visible_options):
                    option_y = y + h * (i + 1)
                    index = i + self.scroll_offset
                    is_hovered = index == self.hover_index
                    fill(*(self.hov if is_hovered else (self.couleur_fond[0]-10 , self.couleur_fond[1]-10 , self.couleur_fond[2]-10)))
                    rect((x, option_y), w, h)
                    fill(*self.couleur_font)
                    text(label, (x + 10, option_y + h / 2))
            pop_style()


    def verifier_clic(self, event):
        """vérifie si on clique sur la zone du menu déroulant"""
        if self.afficher_objet:
            w = self.w * width
            h = self.h * height
            x = self.x * width - w / 2
            y = self.y * height - h / 2
            if self.is_open:
                for i in range(self.max_visible):
                    index = i + self.scroll_offset
                    if index >= len(self.labels):
                        break
                    option_y = y + h * (i + 1)
                    if (x <= event.x <= x + w and option_y <= event.y <= option_y + h):
                        if self.sound:
                            self.sound.jouer()
                        self.selected_index = index
                        self.is_open = False
                        if self.on_select:
                            self.on_select(self.options[self.selected_index])
                        return
                self.is_open = False
            else:

                if (x <= event.x <= x + w and y <= event.y <= y + h):
                    if self.sound:
                        self.sound.jouer()
                    self.is_open = True

    def mouse_moved(self, event):
        """vérifie le mouvement de la souris pour changer la couleur des options survolé"""
        if self.afficher_objet and self.is_open:
            w = self.w * width
            h = self.h * height
            x = self.x * width - w / 2
            y = self.y * height - h / 2
            self.hover_index = -1
            for i in range(self.max_visible):
                index = i + self.scroll_offset
                if index >= len(self.labels):
                    break
                option_y = y + h * (i + 1)
                if (x <= event.x <= x + w and option_y <= event.y <= option_y + h):
                    self.hover_index = index

    def mouse_wheel(self, event):
        """vérifie quand la molette est utilisé pour scroll parmi les options"""
        if self.afficher_objet and self.is_open:
            scroll_direction = event.scroll.y
            if scroll_direction < 0:
                self.scroll_offset = min( self.scroll_offset + 1 , max(0, len(self.options) - self.max_visible) )
            elif scroll_direction > 0:
                self.scroll_offset = max(0, self.scroll_offset - 1)

    def get_selected_option(self):
        """retourne l'option selectionné"""
        return self.options[self.selected_index]

    def get_pixel_position(self):
        return (self.x * width, self.y * height)

    def switch(self):
        """switch de afficher à cacher le menu"""
        self.afficher_objet = not self.afficher_objet

    def cacher(self):
        """cache uniquement le menu"""
        self.afficher_objet = False



class Panel:
    def __init__(self, x, y, w, h, rgba, liste_obj):
        """
        Crée un Panneau qui contient d'autre objet à l'intérieur
        x : position x, int / float
        y : position y, int / float
        w : largeur du panneau, int / float
        h : hauteur du panneau, int / float
        rgba : couleur rgba du panneau, tuple
        liste_obj : liste des objets à afficher avec le panneau, list
        """
        assert type(x) in (int, float), "doit être un int ou float"
        assert type(y) in (int, float), "doit être un int ou float"
        assert type(w) in (int, float), "doit être un int ou float"
        assert type(h) in (int, float), "doit être un int ou float"
        assert type(liste_obj) == list, "doit être une liste"
        assert type(rgba) == tuple, "doit être un tuple"
        for nbr in rgba:
            assert nbr <= 255 and type(nbr) == int,"doit être un tuple de int >=255"
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.rgba = rgba
        self.liste_obj = liste_obj
        self.afficher_objet = False

    def afficher(self):
        """dessine le panneau et affiche tous les objets de la liste des objets"""
        if self.afficher_objet:
            panneau = Rectangle(x=self.x, y=self.y, w=self.w, h=self.h, rgba=self.rgba)
            panneau.afficher()
            for obj in self.liste_obj:
                obj.afficher()

    def _est_dans_zone_dropdown(self, event):
        """Vérifie si un Dropdown est ouvert et si le point (event.x, event.y) est dedans"""
        for obj in self.liste_obj:
            if isinstance(obj, DropdownMenu) and obj.afficher_objet and obj.is_open:
                ## Calcule la zone totale occupée par le menu déroulé
                w = obj.w * width
                h = obj.h * height
                x = obj.x * width - w / 2
                y = obj.y * height - h / 2
                h_total = h * (min(len(obj.labels), obj.max_visible) + 1)
                if x <= event.x <= x + w and y <= event.y <= y + h_total:
                    return True
        return False

    def verifier_clic(self, event):
        """ vérifie l'événement de clique pour tout les éléments du panneau"""
        if self.afficher_objet:
            blocage = self._est_dans_zone_dropdown(event)
            for obj in self.liste_obj:
                if hasattr(obj, 'verifier_clic') and obj.afficher_objet:
                    if not blocage or isinstance(obj, DropdownMenu):
                        obj.verifier_clic(event)

    def mouse_released(self, event):
        """vérifie quand on lache le clique de la souris pour tous les éléments du panneau"""
        if self.afficher_objet:
            blocage = self._est_dans_zone_dropdown(event)
            for obj in self.liste_obj:
                if hasattr(obj, 'mouse_released') and obj.afficher_objet:
                    if not blocage or isinstance(obj, DropdownMenu):
                        obj.mouse_released(event)

    def mouse_dragged(self, event):
        """vérifie quand on maintient le clique de la souris pour tous les éléments du panneau"""
        if self.afficher_objet:
            blocage = self._est_dans_zone_dropdown(event)
            for obj in self.liste_obj:
                if hasattr(obj, 'mouse_dragged') and obj.afficher_objet:
                    if not blocage or isinstance(obj, DropdownMenu):
                        obj.mouse_dragged(event)

    def mouse_moved(self, event):
        """vérifie quand on déplace la souris pour tous les éléments du panneau"""
        if self.afficher_objet:
            blocage = self._est_dans_zone_dropdown(event)
            for obj in self.liste_obj:
                if hasattr(obj, 'mouse_moved') and obj.afficher_objet:
                    if not blocage or isinstance(obj, DropdownMenu):
                        obj.mouse_moved(event)

    def mouse_wheel(self, event):
        """vérifie quand on utilise la molette de la souris pour tous les éléments du panneau"""
        if self.afficher_objet:
            blocage = self._est_dans_zone_dropdown(event)
            for obj in self.liste_obj:
                if hasattr(obj, 'mouse_wheel') and obj.afficher_objet:
                    if not blocage or isinstance(obj, DropdownMenu):
                        obj.mouse_wheel(event)

    def show(self):
        """affiche le panneau de la fenêtre"""
        self.afficher_objet = True

    def cacher(self):
        """cache le panneau de la fenêtre"""
        self.afficher_objet = False




class Fenetre:
    def __init__(self):
        """ crée une classe qui stocke des fenêtre"""
        self.fenetre = {}
        self.fenetre_actuelle = None
        self.afficher_fenetre = True

    def __repr__(self): return str(self.fenetre)

    def ajouter_fenetre(self,nom,obj):
        """
        ajoute une fenetre dans le dictionnaire avec son nom et la liste des objets de la fenetre
        nom : nom de la fenêtre, str
        obj: liste des objet de la fenêtre, list
        """
        assert type(nom) == str,"doit être un str"
        assert type(obj) == list,"doit être une liste"
        self.fenetre[nom] = obj


    def afficher_fenetres(self,nom):
        """
        affiche la fenêtre choisi
        nom : nom de la fenêtre à afficher,str
        """
        assert type(nom) == str,"doit être un str"
        assert nom in self.fenetre.keys(),"doit être une fenêtre initialisé"

        if self.afficher_fenetres:
            for obj in self.fenetre[nom]:
                obj.afficher()

    def cacher_fenetre(self,nom):
        """
        cacher la fenêtre choisi
        nom : nom de la fenêtre à cacher,str
        """
        assert type(nom) == str,"doit être un str"
        assert nom in self.fenetre.keys(),"doit être une fenêtre initialisé"
        for obj in self.fenetre[nom]:
            obj.cacher()

    def show(self,nom):
        """
        utilise la méthode show pour tout les objet de la fenêtre choisi
        nom : nom de la fenêtre à cacher,str
        """
        assert type(nom) == str,"doit être un str"
        assert nom in self.fenetre.keys(),"doit être une fenêtre initialisé"
        for obj in self.fenetre[nom]:
            if hasattr(obj, 'show'):
                if not isinstance(obj, Panel):
                    obj.show()

    def verif(self, event,event1,event2):
        """
        vérifie le clique pour toute les fenetres
        """
        if self.afficher_fenetres:
            for fen in self.fenetre.values():
                for obj in fen:
                    if hasattr(obj, 'verifier_clic') and obj.afficher_objet:
                        obj.verifier_clic(event)
                    elif hasattr(obj,"changer_cellule_sous_souris") and obj.afficher_objet:
                        obj.changer_cellule_sous_souris(event1 , event2)
                        redraw()

    def mouse_released(self,event):
        """vérifie quand on lache le clique de la souris pour tous les éléments de toute les fenêtres"""
        if self.afficher_fenetres:
            for fen in self.fenetre.values():
                for obj in fen:
                    if hasattr(obj, 'mouse_released') and obj.afficher_objet:
                        obj.mouse_released(event)

    def mouse_dragged(self,event):
        """vérifie quand on maintient le clique de la souris pour tous les éléments de toute les fenêtres"""
        if self.afficher_fenetres:
            for fen in self.fenetre.values():
                for obj in fen:
                    if hasattr(obj, 'mouse_dragged') and obj.afficher_objet:
                        obj.mouse_dragged(event)


    def mouse_moved(self,event):
        """vérifie quand on déplace la souris pour tous les éléments de toute les fenêtres"""
        if self.afficher_fenetres:
            for fen in self.fenetre.values():
                for obj in fen:
                    if hasattr(obj, 'mouse_moved') and obj.afficher_objet:
                        obj.mouse_moved(event)

    def mouse_wheel(self,event):
        """vérifie quand on utilise la molette de la souris pour tous les éléments de toute les fenêtres"""
        if self.afficher_fenetres:
            for fen in self.fenetre.values():
                for obj in fen:
                    if hasattr(obj, 'mouse_wheel') and obj.afficher_objet:
                        obj.mouse_wheel(event)

