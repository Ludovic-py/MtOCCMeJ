from tkinter import *
from time import sleep


def conversion_fonction(liste, etape):
    result = []
    indentation = "    " * (etape + 1)
    for j in range(1, len(liste)):
        if j != 1:
            result.append(f"{indentation}{liste[0]},")
        if isinstance(liste[j], list):
            result.append(f"max|{conversion_fonction(liste[j], etape + 1)},")
        else:
            result.append(liste[j])
    return "\n".join(result).rstrip(",")


def conversion_boolean(liste):
    result = []
    for j in range(1, len(liste)):
        if j != 1:
            result.append(f"    {liste[0]}")
        if isinstance(liste[j], list):
            result.append(f"({conversion_boolean(liste[j])})")
        else:
            result.append(liste[j])
    return "".join(result)


def simplify_expression(e, combinator, validate):
    result = [combinator]
    for element in e:
        if element[0] in [combinator, ""]:
            result.extend(element[1:])
        else:
            result.append(element)
    simplified = []
    for i, item in enumerate(result):
        if validate(result, i):
            simplified.append(item)
        else:
            result[i] = "_"
    return simplified


def validate(e0, i):
    current = e0[i]
    existing = e0[:i] + e0[i + 1:]
    if current in existing:
        return False
    elif isinstance(current, list):
        for j in current:
            if j in e0:
                return False
        for k in existing:
            if isinstance(k, list) and not any(j not in k for j in current):
                return False
    return True


def developpement(formule):
    if formule[0] == "":
        return formule
    elif formule[0] == "+":
        return simplify_expression([developpement(e) for e in formule[1:]], "+", validate)
    elif formule[0] == ".":
        return expand_product([developpement(e) for e in formule[1:]])


def expand_product(e):
    result = ["."]
    temp_result = simplify_expression(e, ".", validate)
    for i, term in enumerate(temp_result):
        if isinstance(term, list):
            remaining = temp_result[:i] + temp_result[i + 1:]
            nested_terms = []
            for sub_term in term[1:]:
                if isinstance(sub_term, list):
                    nested_terms.append(expand_product([sub_term, remaining]))
                else:
                    nested_terms.append(expand_product([["", sub_term], remaining]))
            return simplify_expression(nested_terms, "+", validate)
    return result


def factorisation(formule):
    if formule[0] == "":
        return formule
    elif formule[0] == "+":
        return expand_sum([factorisation(e) for e in formule[1:]])
    elif formule[0] == ".":
        return simplify_expression([factorisation(e) for e in formule[1:]], ".", validate)


def expand_sum(e):
    result = ["+"]
    temp_result = simplify_expression(e, "+", validate)
    for i, term in enumerate(temp_result):
        if isinstance(term, list):
            remaining = temp_result[:i] + temp_result[i + 1:]
            nested_terms = []
            for sub_term in term[1:]:
                if isinstance(sub_term, list):
                    nested_terms.append(expand_sum([sub_term, remaining]))
                else:
                    nested_terms.append(expand_sum([["", sub_term], remaining]))
            return simplify_expression(nested_terms, ".", validate)
    return result


class EntreeTaille(Tk):
    def __init__(self, nbcable):
        super().__init__()
        self.resizable(width=False, height=False)
        self.valide = False
        self.nbcable = Variable(self, nbcable)
        Label(self, text="Entrez le nombre de cables :", font=("", 10)).grid(column=0, row=1)
        self.entree = Entry(self, textvariable=self.nbcable, font=("", 10), width=11)
        self.entree.grid(column=1, row=1, pady=5)
        self.entree.focus_force()
        Button(self, text=" Ok ", command=self.retour).grid(column=0, columnspan=2, row=2)
        self._center_window()
        self.bind("<Return>", self.retour)
        self.protocol("WM_DELETE_WINDOW", self.retour)

    def _center_window(self):
        self.update()
        coord = self.geometry().split("+")[0]
        w, h = map(int, coord.split("x"))
        ws, hs = self.winfo_screenwidth(), self.winfo_screenheight()
        x, y = (ws - w) // 2, (hs - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def retour(self, event=None):
        self.valide = True


class Sortie(Tk):
    def __init__(self, canvas, titre, x, y):
        super().__init__()
        self.cnv = canvas
        self.nom = titre
        self.x, self.y = x, y
        self.mode = "boolean"
        self.simplification = "developpement"
        self.text = conversion_boolean(developpement(self.cnv.formules[y][x]))
        self.id_text = Label(self, text=titre + self.text, font=("Consolas", 15))
        self.id_text.pack(expand=True, fill="both")
        self.update_ui()

    def update_ui(self):
        self.menus = Menu(self)
        menu_option = Menu(self.menus, tearoff=0)
        menu_option.add_command(label="Fonction", command=self.fonction)
        menu_option.add_command(label="Boolean", command=self.boolean)
        menu_option.add_separator()
        menu_simplification = Menu(self.menus, tearoff=0)
        menu_simplification.add_command(label="Developpement", command=self.developpement)
        menu_simplification.add_command(label="Factorisation", command=self.factorisation)
        menu_simplification.add_command(label="Aucune", command=self.aucune_simplification)
        menu_option.add_cascade(label="Simplification", menu=menu_simplification)
        self.menus.add_cascade(label="Option", menu=menu_option)
        self.config(menu=self.menus)
        coords = self.geometry().split("+")[0]
        w, h = map(int, coords.split("x"))
        w = max(w, 200)
        ws = self.winfo_screenwidth()
        pos_x = ws - w - 50
        self.geometry(f"{w}x{h}+{pos_x}+100")
        self.protocol("WM_DELETE_WINDOW", self.fermer)

    def actualiser(self):
        if self.simplification == "developpement":
            liste = developpement(self.cnv.formules[self.y][self.x])
        elif self.simplification == "factorisation":
            liste = factorisation(self.cnv.formules[self.y][self.x])
        else:
            liste = self.cnv.formules[self.y][self.x]
        self.text = conversion_boolean(liste) if self.mode == "boolean" else conversion_fonction(liste, 0)
        self.id_text.config(text=self.nom + self.text)
        self.resize_window()

    def resize_window(self):
        height = len(self.text.split("\n")) * 23 + 6
        self.geometry(f"{max(200, len(self.text) * 7)}x{height}")

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

