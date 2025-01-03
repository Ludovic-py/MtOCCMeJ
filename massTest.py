from tkinter import *
from itertools import combinations
from dynamictrusttable import appliquer_logique

## code non fontionnel et bouré d'erreur de logique sur le système de verification à but visuel seulement 
class CableReliabilityApp:
    def __init__(self):
        self.nbcable = None  # Nombre de câbles utilisé par l'utilisateur (initialisé plus tard)
        self.connections = []  # Liste des paires de connexions
        self.result_text = None  # Zone d'affichage des résultats
        self.setup_input()  # Configuration initiale (fenêtre d'entrée utilisateur)

    def setup_input(self):
        """Fenêtre de base pour récupérer le nombre de câbles de l'utilisateur."""
        self.root = Tk()
        self.root.title("Configuration des câbles")
        self.root.resizable(False, False)

        # Label principal
        Label(self.root, text="Entrez le nombre de câbles :", font=("Arial", 14)).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        # Champ d'entrée
        self.cable_input = Entry(self.root, font=("Arial", 14), width=8)
        self.cable_input.grid(row=1, column=0, columnspan=2, pady=10)
        self.cable_input.focus()

        # Bouton pour valider
        Button(
            self.root, text="Suivant", command=self.get_cable_input, font=("Arial", 13)
        ).grid(row=2, column=0, columnspan=2, pady=20)

        self.root.mainloop()

    def get_cable_input(self):
        """Récupération de l'entrée utilisateur et transition vers l'interface principale."""
        try:
            self.nbcable = int(self.cable_input.get())
            if self.nbcable < 2:
                raise ValueError("Le nombre de câbles doit être au moins 2.")
        except ValueError as e:
            Label(self.root, text=f"Saisie invalide : {e}", fg="red").grid(
                row=3, column=0, columnspan=2, pady=10
            )
            return

        # Fermeture de la fenêtre actuelle et lancement de l'interface principale
        self.root.destroy()
        self.setup_main_interface()

    def setup_main_interface(self):
        """Fenêtre principale avec affichage des câbles et calculs."""
        self.root = Tk()
        self.root.title(f"Fiabilité du câblage - {self.nbcable} câbles")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)

        # Titre
        Label(
            self.root,
            text=f"Connexion des câbles - {self.nbcable} Câbles",
            font=("Arial", 18),
        ).pack(pady=20)

        # Espace de connexion des câbles (canvas)
        self.canvas = Canvas(self.root, bg="antique white", height=600, width=1000)
        self.canvas.pack(expand=True, fill="both")

        # Dessiner les câbles
        self.draw_cables()

        # Bouton pour tester les combinaisons
        self.test_button = Button(
            self.root,
            text="Tester les combinaisons",
            command=self.test_all_combinations,
            font=("Arial", 14),
        )
        self.test_button.pack(pady=10)

        # Zone d'affichage des résultats
        self.result_text = Label(self.root, text="", font=("Arial", 14), fg="blue")
        self.result_text.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)  # Gestion de la fermeture
        self.root.mainloop()

    def draw_cables(self):
        """Dessiner les câbles sur le canvas."""
        self.canvas.delete("all")
        spacing = 600 // self.nbcable  # Espacement entre les câbles
        for i in range(self.nbcable):
            y = 100 + i * spacing
            self.canvas.create_line(50, y, 950, y, width=4, fill="black")
            self.canvas.create_text(30, y, text=f"Câble {i + 1}", font=("Arial", 12))

    def generate_possible_connections(self):
        """Génère toutes les connexions possibles entre les câbles."""
        return list(combinations(range(1, self.nbcable + 1), 2))

    def test_all_combinations(self):
        """Tester toutes les combinaisons possibles de connexions."""
        self.connections = self.generate_possible_connections()
        results = []

        # Tester les sous-ensembles
        for size in range(1, len(self.connections) + 1):  # Tailles des combinaisons
            subsets = combinations(self.connections, size)
            for subset in subsets:
                is_reliable = self.is_reliable_combination(subset)
                subset_str = ", ".join(f"({a},{b})" for a, b in subset)
                results.append(f"Combinaison : {subset_str} -> {'Fiable' if is_reliable else 'Non fiable'}")

        self.show_results(results)

    def is_reliable_combination(self, subset):
        """Teste si une combinaison est fiable."""
        # La combinaison est fiable si tous les câbles sont connectés
        connected_cables = set()
        for a, b in subset:
            connected_cables.add(a)
            connected_cables.add(b)
        return len(connected_cables) == self.nbcable

    def show_results(self, results):
        """Afficher les résultats dans une interface déroulante."""
        results_window = Toplevel(self.root)
        results_window.title("Résultats")
        scrollbar = Scrollbar(results_window)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Liste déroulante des résultats
        results_listbox = Listbox(results_window, yscrollcommand=scrollbar.set, font=("Arial", 12))
        results_listbox.pack(fill=BOTH, expand=True)

        for result in results:
            results_listbox.insert(END, result)

        scrollbar.config(command=results_listbox.yview)

    def close_app(self):
        """Fermeture propre de l'application."""
        self.root.destroy()


CableReliabilityApp()
