from tkinter import *
from time import sleep


def conversion_fonction(liste, etape):
    text = ""
    for j in range(1, len(liste)):
        if j != 1:
            text += "    " * (etape+1) + liste[0] + ",\n"
        if type(liste[j]) == list:
            text += "max|" + conversion_fonction(liste, etape+1) + ",\n"
        else:
            text += liste[j] + "\n"
    return text[:-1]


def conversion_boolean(liste):
    text = ""
    for j in range(1, len(liste)):
        if j != 1:
            text += "    " + liste[0]
        if type(liste[j]) == list:
            text += "("+conversion_boolean(liste[j])+")\n"
        else:
            text += liste[j] + "\n"
    return text[:-1]


def developpement(formule):
    def est_valide(e0, i):
        if e0[i] in e0[:i] + e0[i + 1:]:  # s'il ne se répète pas (x+x=x et x.x=x avec +<=>ou & .<=>et)
            return False
        elif type(e0[i]) == list:  # si c'est un type différent de l'opération (x+(y.z) ou x.(y+z))
            for j in e0[i]:
                if j in e0:  # simplifie x+(x.y) (=x) et x.(x+y) (=x)
                    return False
            for k in e0[:i] + e0[i + 1:]:
                if type(k) == list:
                    state = False
                    for j in k:
                        if j not in e0[i]:
                            state = True
                    if state is False:  # simplifie (x.y.z)+(x.y) (=(x.y)) et (x+y+z).(x+y) (=(x+y))
                        return False
        return True

    def s(e):  # Somme des termes contenus dans la liste d'entrée
        e0 = ["+"]
        for i in range(len(e)):  # regroupement dans la même liste de tous les termes additionnés
            if e[i][0] in ["+", ""]:
                e0 += e[i][1:]
            else:
                e0.append(e[i])
        e1 = []
        for i in range(len(e0)):  # vérification de tous les termes (s'ils ne se répètent pas)
            if est_valide(e0, i):
                e1.append(e0[i])
            else:
                e0[i] = "_"
        return e1

    def m(e):  # Multiplication des termes contenus dans la liste d'entrée
        e0 = ["."]
        for i in range(len(e)):  # regroupement dans la même liste de tous les termes multipliés
            if e[i][0] in [".", ""]:
                e0 += e[i][1:]
            else:
                e0.append(e[i])
        e1 = []
        for i in range(len(e0)):  # vérification de tous les termes (s'ils ne se répètent pas)
            if est_valide(e0, i):
                e1.append(e0[i])
            else:
                e0[i] = "_"
        for i in range(len(e1)):
            if type(e1[i]) == list:  # développement !!!!!
                e2 = e1[:i] + e1[i + 1:]  # le reste des facteurs
                if len(e2) == 2:
                    if type(e2[1]) == list:
                        e2 = e2[1]
                    else:
                        e2[0] = ""
                e3 = []  # 1) Un développement c'est ...
                for j in e1[i][1:]:
                    if type(j) == list:
                        e3.append(m([j, e2]))  # 4) (la double distributivité est un développement de développement)
                    else:
                        e3.append(m([["", j], e2]))  # 3) ... de la multiplication des termes entre eux.
                return s(e3)  # 2) ... l'addition ...
        return e1

    if formule[0] == "":
        return formule
    elif formule[0] == "+":
        e1 = s([developpement(i) for i in formule[1:]])
        return e1
    elif formule[0] == ".":
        e1 = m([developpement(i) for i in formule[1:]])
        return e1


def factorisation(formule):
    def est_valide(e0, i):
        if e0[i] in e0[:i] + e0[i + 1:]:  # s'il ne se répète pas (x+x=x et x.x=x avec +<=>ou & .<=>et)
            return False
        elif type(e0[i]) == list:  # si c'est un type différent de l'opération (x+(y.z) ou x.(y+z))
            for j in e0[i]:
                if j in e0:  # simplifie x+(x.y) (=x) et x.(x+y) (=x)
                    return False
            for k in e0[:i] + e0[i + 1:]:
                if type(k) == list:
                    state = False
                    for j in k:
                        if j not in e0[i]:
                            state = True
                    if state is False:  # simplifie (x.y.z)+(x.y) (=(x.y)) et (x+y+z).(x+y) (=(x+y))
                        return False
        return True

    def s(e):  # Addition des termes contenus dans la liste d'entrée
        e0 = ["+"]
        for i in range(len(e)):  # regroupement dans la même liste de tous les termes additionné
            if e[i][0] in ["+", ""]:
                e0 += e[i][1:]
            else:
                e0.append(e[i])
        e1 = []
        for i in range(len(e0)):  # vérification de tous les termes (s'ils ne se répètent pas)
            if est_valide(e0, i):
                e1.append(e0[i])
            else:
                e0[i] = "_"
        for i in range(len(e1)):
            if type(e1[i]) == list:  # factorisation !!!!!
                e2 = e1[:i] + e1[i + 1:]  # le reste des facteurs
                if len(e2) == 2:
                    if type(e2[1]) == list:
                        e2 = e2[1]
                    else:
                        e2[0] = ""
                e3 = []  # 1) Une factorisation c'est ...
                for j in e1[i][1:]:
                    if type(j) == list:
                        e3.append(s([j, e2]))
                    else:
                        e3.append(s([["", j], e2]))  # 3) ... de l'addition des termes entre eux.
                return m(e3)  # 2) ... la multiplication ...
        return e1

    def m(e):  # Multiplication des termes contenus dans la liste d'entrée
        e0 = ["."]
        for i in range(len(e)):  # regroupement dans la même liste de tous les termes multiplié
            if e[i][0] in [".", ""]:
                e0 += e[i][1:]
            else:
                e0.append(e[i])
        e1 = []
        for i in range(len(e0)):  # vérification de tous les termes (s'ils ne se répètent pas)
            if est_valide(e0, i):
                e1.append(e0[i])
            else:
                e0[i] = "_"
        return e1

    if formule[0] == "":
        return formule
    elif formule[0] == "+":
        e1 = s([developpement(i) for i in formule[1:]])
        return e1
    elif formule[0] == ".":
        e1 = m([developpement(i) for i in formule[1:]])
        return e1


class EntreeTaille(Tk):
    def __init__(self, nbcable):
        Tk.__init__(self)
        self.resizable(width=False, height=False)

        self.valide = False
        self.nbcable = Variable(self, nbcable)

        self.label = Label(self, text="Entrez le nombre de cables :", font=("", 10))
        self.label.grid(column=0, row=1)

        self.entree = Entry(self, textvariable=self.nbcable, font=("", 10), width=11)
        self.entree.grid(column=1, row=1, pady=5)
        self.entree.focus_force()

        self.bouton = Button(self, text=" Ok ", command=self.retour)
        self.bouton.grid(column=0, columnspan=2, row=2)

        # Place the Window in the middle of the screen
        self.update()
        coord = self.geometry().split("+")[0]
        w, h = coord.split("x")
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws - int(w)) // 2
        y = (hs - int(h)) // 2
        self.geometry("%sx%s+%d+%d" % (w, h, x, y))

        self.bind("<Return>", self.retour)
        self.protocol("WM_DELETE_WINDOW", self.retour)

    def retour(self, event=None):
        self.valide = True


class Sortie(Tk):
    def __init__(self, canvas, titre, x, y):
        Tk.__init__(self)
        # self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.title(titre)

        self.cnv = canvas
        self.nom = titre
        print(x)
        print(y)
        self.x = x
        self.y = y
        self.mode = "boolean"
        self.simplification = "developpement"

        self.menus = Menu(self)
        #
        self.menu_option = Menu(self.menus, tearoff=0)
        self.menu_option.add_command(label="Fonction", command=self.fonction)
        self.menu_option.add_command(label="Boolean", command=self.boolean)
        self.menu_option.add_separator()
        ##
        self.menu_simplification = Menu(self.menus, tearoff=0)
        self.menu_simplification.add_command(label="Developpement", command=self.developpement)
        self.menu_simplification.add_command(label="Factorisation", command=self.factorisation)
        self.menu_simplification.add_command(label="Aucune", command=self.aucune_simplification)
        self.menu_option.add_cascade(label="Simplification", menu=self.menu_simplification)
        ##
        self.menus.add_cascade(label="Option", menu=self.menu_option)
        #
        self.config(menu=self.menus)

        self.text = conversion_boolean(developpement(self.cnv.formules[y][x]))
        self.id_text = Label(self, text=titre+self.text, font=("Consolas", 15))
        self.id_text.pack(expand=True, fill="both")

        self.update()
        coords = self.geometry().split("+")[0]
        w, h = coords.split("x")
        if int(w) < 200:
            w = "200"
        ws = self.winfo_screenwidth()
        x = ws - int(w) - 50
        self.geometry("%sx%s+%d+%d" % (w, h, x, 100))
        self.update()

        self.protocol("WM_DELETE_WINDOW", self.fermer)

    def deplacer(self, cx, delta_nbc):
        if self.x >= cx:
            self.x += delta_nbc
            if self.x == -1:
                self.destroy()
            else:
                self.cnv.sorties[self.y][self.x] = self
            self.cnv.sorties[self.y][self.x-delta_nbc] = None
            if self.x != self.cnv.nbcollones:
                self.nom = "%d;%d :" % (self.x, self.y+1)
            self.title(self.nom)
            print(self.x)

    def actualiser(self):
        if self.simplification == "developpement":
            liste = developpement(self.cnv.formules[self.y][self.x])
        elif self.simplification == "factorisation":
            liste = factorisation(self.cnv.formules[self.y][self.x])
        else:
            liste = self.cnv.formules[self.y][self.x]

        if self.mode == "fonction":
            self.text = conversion_fonction(liste, 0)
        elif self.mode == "boolean":
            self.text = conversion_boolean(liste)

        print(self.text)
        self.id_text.config(text=self.nom+self.text)
        taille, x, y = self.geometry().split("+")
        w, h = taille.split("x")
        h = len(self.text.split("\n")) * 23 + 6
        if int(w) < 200:
            w = "200"
        ws = self.winfo_screenwidth()
        if int(x) + int(w) > ws - 50:
            x = str(ws - int(w) - 50)
        self.geometry("%sx%s+%s+%s" % (w, h, x, y))
        self.update()

    def fonction(self):
        self.mode = "fonction"
        self.actualiser()

    def boolean(self):
        self.mode = "boolean"
        self.actualiser()

    def developpement(self):
        self.simplification = "developpement"
        self.actualiser()

    def factorisation(self):
        self.simplification = "factorisation"
        self.actualiser()

    def aucune_simplification(self):
        self.simplification = "aucune"
        self.actualiser()

    def fermer(self):
        self.cnv.sorties[self.y][self.x] = None
        self.destroy()


class Lien:
    def __init__(self, canvas, x, y1, y2):
        self.cnv = canvas
        self.x = x
        self.y1 = y1
        self.y2 = y2
        pas = (self.cnv.ws-self.cnv.g-self.cnv.d)//(self.cnv.nbcollones+1)
        self.trait = self.cnv.create_line(self.cnv.g + (self.x+1) * pas, self.cnv.g + self.y1 * self.cnv.Ecart,
                                          self.cnv.g + (self.x+1) * pas, self.cnv.g + self.y2 * self.cnv.Ecart,
                                          fill="grey", width=5)
        self.cercle1 = self.cnv.create_oval(self.cnv.g + (self.x+1)*pas - 10, self.cnv.g + self.y1*self.cnv.Ecart - 10,
                                            self.cnv.g + (self.x+1)*pas + 10, self.cnv.g + self.y1*self.cnv.Ecart + 10,
                                            fill="grey")
        self.cercle2 = self.cnv.create_oval(self.cnv.g + (self.x+1)*pas - 10, self.cnv.g + self.y2*self.cnv.Ecart - 10,
                                            self.cnv.g + (self.x+1)*pas + 10, self.cnv.g + self.y2*self.cnv.Ecart + 10,
                                            fill="grey")

    def getx(self):
        return self.x

    def gety1(self):
        return self.y1

    def gety2(self):
        return self.y2

    def delete(self):
        self.cnv.delete(self.cercle1)
        self.cnv.delete(self.trait)
        self.cnv.delete(self.cercle2)

    def deplacer(self, cx, delta_nbc):
        old_pas = (self.cnv.ws - self.cnv.g - self.cnv.d) // (self.cnv.nbcollones + 1 - delta_nbc)
        pas = (self.cnv.ws - self.cnv.g - self.cnv.d) // (self.cnv.nbcollones + 1)
        if self.x >= cx:
            self.x += delta_nbc
            vx = (self.x+1) * pas - (self.x+1-delta_nbc) * old_pas
        else:
            vx = (self.x+1) * pas - (self.x+1) * old_pas
        self.cnv.move(self.trait, vx, 0)
        self.cnv.move(self.cercle1, vx, 0)
        self.cnv.move(self.cercle2, vx, 0)


class MainWindow(Canvas):
    def __init__(self):
        # Create the Window
        self.root = Tk()
        self.root.state("zoomed")  # elle est agrandie
        self.root.title("Cable")  # actualise le titre de la fenetre
        self.root.focus_set()  # elle prend le focus par défaut
        self.ws = self.root.winfo_screenwidth()
        self.hs = self.root.winfo_screenheight()
        self.g = 100  # écart au bord gauche et en haut du canvas
        self.d = 100  # écart au bord droit du canvas

        # Create the canvas
        Canvas.__init__(self, self.root, bg="light blue")
        self.pack(expand=True, fill="both")  # le canvas occupe toute la fenetre

        # Initiate the variables
        self.nbcable = 6  # nombre de cables par défaut lors du lancement du programme (nb de ligne dans la matrice)
        self.nbcollones = 0  # nombre de collones dans la matrice
        self.formules = [[]]  # matrice qui regroupe l'état de chaque segment de cables
        self.listCable = []  # liste qui regroupe les identifiants de tout les cables tracé sur le canvas
        self.listLien = []  # liste qui regroupe toutes les collones de liens
        self.sorties = [[]]  # matrice qui regroupe toutes les sorties actives, None si rien
        self.Ecart = 100  # écart entre les cables
        self.curseur = 0  # id du curseur sur le canvas, à 0 si non affiché
        self.cx = 0  # coordonnée x du curseur, à 0 si non affiché
        self.cy = 0  # coordonnée y du curseur, à 0 si non affiché
        self.fiabilite = 0  # identifiant de l'indicateur de fiabilité sur le canvas
        self.indications = 0  # identifiant des consignes sur le canvas

        # Create the button
        self.nouveau = Button(self.root, text="Changer", font=("Consolas", 15), command=self.commencer)
        self.nouveau.place(x=self.ws // 2, y=self.hs - 150, anchor="center")  # place le bouton en bas / au milieu

        self.commencer()

        # Make event work
        self.root.bind("<Return>", self.commencer)
        self.root.bind("<Button-1>", self.clic_gauche)
        self.root.bind("<Button-3>", self.clic_droit)
        self.root.protocol("WM_DELETE_WINDOW", self.fermer)

        # Make the window work
        self.root.mainloop()

    def commencer(self, event=None):
        # réinitialisation des données
        self.delete(ALL)
        self.listLien = []
        for liste in self.sorties:
            for sortie in liste:
                if sortie is not None:
                    sortie.destroy()  # suprime toutes les fenetres de sorties
        self.nbcollones = 0
        self.fiabilite = self.create_text(self.ws // 4, self.hs - 150, fill="black", anchor="center",
                                          font=("Consolas", 15), text="Le cablage n'est pas fiable.")
        self.indications = self.create_text(self.ws-200, 50, fill="black", anchor="n", font=("Consolas", 15),
                                            text="Clic gauche sur un cable\n"
                                                 "puis sur un autre\n"
                                                 "(l'un au dessus de l'autre)\n"
                                                 "pour créer un nouveau lien.\n"
                                                 "\n"
                                                 "Clic gauche sur un lien\n"
                                                 "pour supprimer ce lien.\n"
                                                 "\n"
                                                 "Clic droit sur un cable\n"
                                                 "pour créer une fenêtre qui affiche\n"
                                                 "l'état de ce cable à cet endroit\n"
                                                 "selon plusieurs modes :\n"
                                                 "fonction / booléen\n"
                                                 "et selon plusieurs modes\n"
                                                 "de simplification :\n"
                                                 "développement / factorisation /\n"
                                                 "aucune simplification.\n"
                                                 "\n"
                                                 "Ces paramètres sont réglable\n"
                                                 "dans les options de la fenêtre\n"
                                                 "de sortie.")

        # Create a window for the entres
        entre = EntreeTaille(self.nbcable)
        while not entre.valide:  # boucle de fonctionnement de la fenetre d'entrée
            entre.update()
            entre.update_idletasks()
            sleep(0.01)
        # quand la fenetre d'entrée est fermée / validé, récupère l'état de la variable et détruit la fenêtre
        self.nbcable = int(entre.nbcable.get())
        entre.destroy()

        # re-initialise les matrices avec la nouvelle valeur
        self.sorties = [[None] for _ in range(self.nbcable)]
        self.formules = [[["", "A%d" % (i+1)]] for i in range(self.nbcable)]

        self.g = 50  # écart des cables par rapport au bord haut et gauche (=> g)
        self.d = 400  # écart des cables par rapport au bord droit (=> d)
        self.Ecart = (self.hs - 250) // self.nbcable  # re-ajuste la valeur de l'écart entre les cables
        self.listCable = [self.create_line(self.g, self.g + i*self.Ecart,  # crée les cables sur le canvas
                          self.ws - self.d, self.g + i*self.Ecart, width=5) for i in range(self.nbcable)]

    def est_superposable(self, x, y1, y2):  # vérifie si on peut regrouper des cables dans la même collone
        if 0 > x or x > self.nbcollones-1:
            return False
        for lien in self.listLien[x]:
            if y1 <= lien.gety2() and lien.gety1() <= y2:
                return False
        return True

    def creer_lien(self, x, y):
        def inserer_dans_collone(x2):
            indice = 0
            for lien in self.listLien[x2]:
                if lien.gety2() < min(self.cy, y):
                    indice += 1
            self.listLien[x2].insert(indice, Lien(self, x2, min(self.cy, y), max(self.cy, y)))

        if self.cx == x and self.cy != y:
            if self.est_superposable(self.cx - 1, min(self.cy, y), max(self.cy, y)):
                inserer_dans_collone(self.cx - 1)
            elif self.est_superposable(self.cx, min(self.cy, y), max(self.cy, y)) and self.nbcollones != 0:
                inserer_dans_collone(self.cx)
            else:
                self.nbcollones += 1

                for liste in self.listLien:
                    for lien in liste:
                        lien.deplacer(self.cx, 1)
                self.listLien.insert(self.cx, [Lien(self, self.cx, min(self.cy, y), max(self.cy, y))])

                for i in range(self.nbcable):
                    self.sorties[i].insert(self.cx, None)
                for liste in self.sorties:
                    for sortie in liste:
                        if sortie is not None:
                            sortie.deplacer(self.cx, 1)
            self.actualiser()

    def clic_gauche(self, event):
        def afficher_curseur():
            self.cy = cy
            self.cx = cx
            self.curseur = self.create_oval(self.g + (self.cx+0.5) * pas - 10,
                                            self.g + self.cy * self.Ecart - 10,
                                            self.g + (self.cx+0.5) * pas + 10,
                                            self.g + self.cy * self.Ecart + 10,
                                            fill="red", width=0)

        def supprimer_lien():
            x = (event.x - (self.g - 5)) // pas - 1
            y = (event.y - self.g) // self.Ecart + 1
            est_seul = True
            idlien = None
            for lien in self.listLien[x]:
                if lien.gety1() <= y <= lien.gety2():
                    idlien = lien
                else:
                    est_seul = False
            if idlien is not None:
                idlien.delete()
                self.listLien[x].remove(idlien)
                if est_seul is True:
                    self.nbcollones -= 1

                    for liste in self.listLien:
                        for lien in liste:
                            lien.deplacer(x, -1)
                    self.listLien.remove([])

                    for liste in self.sorties:
                        for sortie in liste:
                            if sortie is not None:
                                sortie.deplacer(x, -1)
                    for i in range(self.nbcable):
                        self.sorties[i].pop(self.nbcollones + 1)
                self.actualiser()
        # ==============================================================================================================
        pas = (self.ws-self.g-self.d)//(self.nbcollones+1)
        est_sur_ligne = (event.y - (self.g - 10)) % self.Ecart < 20 and self.g < event.x < self.ws - self.d
        est_sur_lien = (event.x - (self.g - 10)) % pas < 20
        cx = (event.x - self.g) // pas
        cy = (event.y - (self.g - 10)) // self.Ecart
        if est_sur_ligne and 0 <= cy < self.nbcable:
            if self.curseur == 0:  # si le curseur n'est pas affiché
                afficher_curseur()
            else:
                self.creer_lien(cx, cy)
                self.delete(self.curseur)
                self.cy, self.cx, self.curseur = 0, 0, 0
        elif est_sur_lien:
            supprimer_lien()

    def clic_droit(self, event):
        pas = (self.ws-self.g-self.d)//(self.nbcollones+1)
        est_sur_ligne = (event.y - (self.g - 10)) % self.Ecart < 20 and self.g < event.x < self.ws - self.d
        y, x = (event.y - (self.g - 10)) // self.Ecart, (event.x - self.g) // pas
        if est_sur_ligne and 0 <= y < self.nbcable:
            if x == self.nbcollones:
                nom = "S%d=  " % (y+1)
            else:
                nom = "%d;%d :" % (x, y+1)
            if self.sorties[y][x] is not None:
                self.sorties[y][x].destroy()
            self.sorties[y][x] = Sortie(self, nom, x, y)

    def calcul(self):
        def is_lien():
            for lien in self.listLien[x]:
                if lien.gety1() == y or lien.gety2() == y:
                    return lien
            return None

        self.formules = [[["", "A%d" % (i+1)]] for i in range(self.nbcable)]
        for x in range(self.nbcollones):
            for y in range(self.nbcable):
                lien = is_lien()
                if lien:
                    if lien.gety1() == y:
                        self.formules[y].append(["+", self.formules[y][x], self.formules[lien.gety2()][x]])
                    elif lien.gety2() == y:
                        self.formules[y].append([".", self.formules[lien.gety1()][x], self.formules[y][x]])
                else:
                    self.formules[y].append(self.formules[y][x])

    def est_fiable(self):
        def etat():
            def is_lien():
                for lien in self.listLien[x]:
                    if lien.gety1() == y or lien.gety2() == y:
                        return lien
                return None

            etats = [[entree[i]] for i in range(self.nbcable)]
            for x in range(self.nbcollones):
                for y in range(self.nbcable):
                    lien = is_lien()
                    if lien:
                        if lien.gety1() == y:
                            etats[y].append(max(etats[y][x], etats[lien.gety2()][x]))
                        elif lien.gety2() == y:
                            etats[y].append(min(etats[lien.gety1()][x], etats[y][x]))
                    else:
                        etats[y].append(etats[y][x])
            return [etats[j][self.nbcollones] for j in range(self.nbcable)]

        for i in range(2**self.nbcable):
            entree = [0 for _ in range(self.nbcable)]
            d = i
            for E in range(self.nbcable):
                entree[E] = d // 2 ** (self.nbcable - E - 1)
                d = d % 2 ** (self.nbcable - E - 1)
            sortie = etat()
            a = sortie[0]
            for j in range(1, self.nbcable):
                if sortie[j] > a:
                    return False
                a = sortie[j]
        return True

    def actualiser(self):
        self.calcul()

        for liste in self.sorties:
            for sortie in liste:
                if sortie is not None:
                    sortie.actualiser()

        if self.est_fiable():
            self.itemconfig(self.fiabilite, text="Le cablage est fiable.")
        else:
            self.itemconfig(self.fiabilite, text="Le cablage n'est pas fiable.")

    def fermer(self):
        for liste in self.sorties:
            for sortie in liste:
                if sortie is not None:
                    sortie.destroy()
        self.root.destroy()


cnv = MainWindow()
