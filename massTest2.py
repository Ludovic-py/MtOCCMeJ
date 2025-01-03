from tkinter import *
from itertools import combinations
from dynamictrusttable import appliquer_logique

## code non fontionnel et bouré d'erreur de logique(au moins autant que dans massTest)sur le système de verification à but visuel seulement 


class CableReliabilityApp:
    def __init__(self):
        self.nbcable = None  # nombre de cables quon utilise
        self.connections = []  # liste des paires de connections
        self.result_text = None  # Label to display results
        self.setup_input()  # l'input debut pour donner le nombre de cables

    def setup_input(self):
        """la fenetre pour ecrire le nombre de cable"""
        self.root = Tk()
        self.root.title("Cable Reliability Input")
        self.root.resizable(False, False)

        # le label
        Label(self.root, text="Number of cables:", font=("Arial", 14)).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        # l'entrée de texte, enfin l'imput quoi
        self.cable_input = Entry(self.root, font=("Arial", 14), width=8)
        self.cable_input.grid(row=1, column=0, columnspan=2, pady=10)
        self.cable_input.focus()

        # bouton submit/suivant
        Button(
            self.root, text="Suivant", command=self.get_cable_input, font=("Arial", 13)
        ).grid(row=2, column=0, columnspan=2, pady=20)

        self.root.mainloop()

    def get_cable_input(self):
        """je recup la saisie+ je passe a la fenettre/app principale"""
        try:
            self.nbcable = int(self.cable_input.get())
            if self.nbcable < 2:
                raise ValueError("nombre de cable doit être d'au moins 2.")
        except ValueError as e:
            Label(self.root, text=f"Invalid input: {e}", fg="red").grid(
                row=3, column=0, columnspan=2, pady=10
            )
            return

        # ferme la fenetre d'input et lance le main
        self.root.destroy()
        self.setup_main_interface()

    def setup_main_interface(self):
        """fenettre principale, me semble un peu inutile maintenant que j'ai terminé"""
        self.root = Tk()
        self.root.title(f"Cable Reliability Study - {self.nbcable} Cables")
        self.root.state("zoomed")
        self.root.resizable(True, True)

        # le titre de l'app/fenettre
        Label(
            self.root,
            text=f"Cable Connections and Reliability - {self.nbcable} Cables",
            font=("Arial", 18),
        ).pack(pady=20)

        self.canvas = Canvas(self.root, bg="antique white", height=600, width=1000)
        self.canvas.pack(expand=True, fill="both")

        # je dessine les cables comme dans to programme raph
        self.draw_cables()

        # bouton pour lancer le calcul
        self.test_button = Button(
            self.root,
            text="Tester toute les Combinaisons",
            command=self.test_all_combinations,
            font=("Arial", 14),
        )
        self.test_button.pack(pady=10)

        # la fenetre/ecran/app/jspquoid'autre pour les resultats
        self.result_text = Label(self.root, text="", font=("Arial", 14), fg="blue")
        self.result_text.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.close_app)
        self.root.mainloop()

    def draw_cables(self):
        self.canvas.delete("all")
        spacing = 600 // self.nbcable  # distance entre les cables
        for i in range(self.nbcable):
            # hop ca dessine cable par cable
            y = 100 + i * spacing
            self.canvas.create_line(50, y, 950, y, width=4, fill="black")
            self.canvas.create_text(30, y, text=f"Cable {i + 1}", font=("Arial", 12))

    def generate_possible_connections(self):
        """genere une listed es connection possible (des paire genre (1,2) ou (1,3))"""
        return list(combinations(range(1, self.nbcable + 1), 2))

    def test_all_combinations(self):
        """Test all subsets of connections for the given number of cables."""
        self.connections = self.generate_possible_connections()
        results = []

        for size in range(1, len(self.connections) + 1): 
            subsets = combinations(self.connections, size)
            for subset in subsets:
                is_reliable = self.is_reliable_combination(subset)
                subset_str = ", ".join(f"({a},{b})" for a, b in subset)
                results.append(f"Combination: {subset_str} -> {'Reliable' if is_reliable else 'Unreliable'}")

        # ecrit les resultats
        self.show_results(results)

    def is_reliable_combination(self, subset):
        # à refaire car inutille sinon

    def show_results(self, results):
        # j'efface les resultats precedends avant d'aficher les nouveaux (pas utile là (vu quon peut pas faire plusieurs test l'un apres l'autre)mais va servir plus tard avec des boutons supl)
        if self.result_text:
            self.result_text.destroy()

        # met le truck pour pouvoir scroller
        results_window = Toplevel(self.root)
        results_window.title("Results")
        scrollbar = Scrollbar(results_window)
        scrollbar.pack(side=RIGHT, fill=Y)

        # liste des resultats
        results_listbox = Listbox(results_window, yscrollcommand=scrollbar.set, font=("Arial", 12))
        results_listbox.pack(fill=BOTH, expand=True)

        for result in results:
            results_listbox.insert(END, result)

        scrollbar.config(command=results_listbox.yview)
    # truc basique ferme l'app si tu clique sur fermer ( pas nessesaire sur windows je crois mais vu que je suis sur un macbook quand je ferme ça reste allumé en arière plan :( )
    def close_app(self):
        self.root.destroy()


CableReliabilityApp()
