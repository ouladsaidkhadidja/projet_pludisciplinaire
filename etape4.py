import tkinter as tk
from tkinter import filedialog, messagebox, Menu, ttk
import matplotlib.pyplot as plt
import numpy as np
import os

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Traceur Polaire Plan E H")
        self.root.geometry("600x400")

        self.planEPath = None
        self.planHPath = None
        self.echelleVar = tk.DoubleVar(value=1.0)
        self.offsetVar = tk.DoubleVar(value=0.0)
        self.lastFigure = None

        self.creerMenu()
        self.creerWidgets()

    def creerMenu(self):
        menubar = Menu(self.root)

        fichier = Menu(menubar, tearoff=0)
        fichier.add_command(label="Charger Fichier Plan E", command=self.chargerPlanE)
        fichier.add_command(label="Charger Fichier Plan H", command=self.chargerPlanH)
        fichier.add_separator()
        fichier.add_command(label="Quitter", command=self.root.quit)
        menubar.add_cascade(label="Fichier", menu=fichier)

        affichage = Menu(menubar, tearoff=0)
        affichage.add_command(label="Tracer", command=self.tracer)
        menubar.add_cascade(label="Affichage", menu=affichage)

        self.root.config(menu=menubar)

    def creerWidgets(self):
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(fill=tk.BOTH, expand=True)

        self.labelFichierE = tk.Label(frame, text="Fichier Plan E : Non chargé", fg="gray")
        self.labelFichierE.pack(anchor='w')

        self.labelFichierH = tk.Label(frame, text="Fichier Plan H : Non chargé", fg="gray")
        self.labelFichierH.pack(anchor='w')

        tk.Label(frame, text="Échelle :").pack(anchor='w', pady=(10, 0))
        tk.Entry(frame, textvariable=self.echelleVar, width=10).pack(anchor='w')

        tk.Label(frame, text="Offset :").pack(anchor='w', pady=(10, 0))
        tk.Entry(frame, textvariable=self.offsetVar, width=10).pack(anchor='w')

        tk.Label(frame, text="Choisir le plan à tracer :").pack(anchor='w', pady=(10, 0))
        options = ["Plan E", "Plan H", "Les deux"]
        self.planSelectionne = ttk.Combobox(frame, values=options, state="readonly")
        self.planSelectionne.set("Les deux")
        self.planSelectionne.pack(anchor='w')

        tk.Button(frame, text="Tracer", command=self.tracer, bg="#3366cc", fg="white").pack(pady=10)
        tk.Button(frame, text="Enregistrer", command=self.enregistrer, bg="green", fg="white").pack()

    def chargerPlanE(self):
        path = filedialog.askopenfilename(title="Charger un fichier pour le Plan E", filetypes=[("Fichiers texte", "*.txt")])
        if path:
            self.planEPath = path
            self.labelFichierE.config(text=f"Fichier Plan E : {os.path.basename(path)}", fg="green")

    def chargerPlanH(self):
        path = filedialog.askopenfilename(title="Charger un fichier pour le Plan H", filetypes=[("Fichiers texte", "*.txt")])
        if path:
            self.planHPath = path
            self.labelFichierH.config(text=f"Fichier Plan H : {os.path.basename(path)}", fg="green")

    def chargerDonnees(self, chemin):
        with open(chemin, "r") as f:
            contenu = f.read()
            morceaux = contenu.replace(",", " ").split()
            valeurs = []

            for val in morceaux:
                try:
                    valeurs.append(float(val))
                except ValueError:
                    continue

        if len(valeurs) not in [144, 720]:
            raise ValueError(f"Le fichier doit contenir 144 ou 720 valeurs, trouvé {len(valeurs)} valeurs.")

        moitie = len(valeurs) // 2
        planEVal = valeurs[:moitie]
        planHVal = valeurs[moitie:]

        return planEVal, planHVal

    def tracer(self):
        choix = self.planSelectionne.get()

        if choix == "Les deux":
            if not self.planEPath or not self.planHPath:
                messagebox.showerror("Erreur", "Les deux fichiers (Plan E et Plan H) doivent être chargés.")
                return

            try:
                planEVal, _ = self.chargerDonnees(self.planEPath)
                _, planHVal = self.chargerDonnees(self.planHPath)
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire les données : {e}")
                return

            self.lastFigure = plt.figure(figsize=(12, 6))

            ax1 = self.lastFigure.add_subplot(121, polar=True)
            self.plot(ax1, planEVal, "Plan E", "blue")
            ax1.set_title("Plan E - Affichage Polaire")

            ax2 = self.lastFigure.add_subplot(122, polar=True)
            self.plot(ax2, planHVal, "Plan H", "red")
            ax2.set_title("Plan H - Affichage Polaire")

            plt.tight_layout()
            plt.show()

        else:
            if choix == "Plan E" and not self.planEPath:
                messagebox.showerror("Erreur", "Le fichier Plan E doit être chargé.")
                return
            if choix == "Plan H" and not self.planHPath:
                messagebox.showerror("Erreur", "Le fichier Plan H doit être chargé.")
                return

            try:
                if choix == "Plan E":
                    planEVal, _ = self.chargerDonnees(self.planEPath)
                    self.lastFigure = plt.figure(figsize=(8, 6))
                    ax = self.lastFigure.add_subplot(111, polar=True)
                    self.plot(ax, planEVal, "Plan E", "blue")
                    ax.set_title("Plan E - Affichage Polaire")
                    plt.tight_layout()
                    plt.show()

                elif choix == "Plan H":
                    _, planHVal = self.chargerDonnees(self.planHPath)
                    self.lastFigure = plt.figure(figsize=(8, 6))
                    ax = self.lastFigure.add_subplot(111, polar=True)
                    self.plot(ax, planHVal, "Plan H", "red")
                    ax.set_title("Plan H - Affichage Polaire")
                    plt.tight_layout()
                    plt.show()

            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible de lire les données : {e}")
                return

    def plot(self, ax, valeurs, label, couleur):
        pas = 1 if len(valeurs) == 360 else 5

        indexMax = np.argmax(valeurs)
        valeurs = valeurs[indexMax:] + valeurs[:indexMax]

        angles = np.deg2rad([i * pas for i in range(len(valeurs))])
        rayons = [(v + self.offsetVar.get()) * self.echelleVar.get() for v in valeurs]

        ax.plot(angles, rayons, marker='o', markersize=2, linewidth=1, label=label, color=couleur)
        ax.legend(loc='upper right')
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
        ax.grid(True)

    def enregistrer(self):
        if self.lastFigure is None:
            messagebox.showinfo("Info", "Aucun graphique à enregistrer.")
            return

        chemin = filedialog.asksaveasfilename(defaultextension=".png",
                                              filetypes=[("Image PNG", "*.png")],
                                              title="Enregistrer sous")
        if chemin:
            try:
                self.lastFigure.savefig(chemin, dpi=300)
                messagebox.showinfo("Succès", f"Graphique enregistré :\n{chemin}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer : {e}")

if __name__ == "__main__":
    racine = tk.Tk()
    app = App(racine)
    racine.mainloop()
