import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.ndimage import gaussian_filter1d

# Création de la fenêtre principale
root = tk.Tk()
root.title("Affichage de Graphe Polaire")
root.geometry("900x650")

# Variables globales
file = ""
v_horizontal, v_vertical = [], []
dh_horizontal, dh_vertical = "", ""
figure, canvas = None, None

# Paramètres utilisateur
step = tk.StringVar(value="1")
m = tk.StringVar(value="2D")
smooth = tk.BooleanVar(value=False)

default_view = {"elev": 30, "azim": -60}

# Lecture du fichier
def readfile(fichier):
    global v_horizontal, v_vertical, dh_horizontal, dh_vertical
    try:
        with open(fichier, "r") as f:
            lignes = f.readlines()

        if len(lignes) < 726:
            messagebox.showerror("Erreur", "Le fichier est incomplet. Il faut au moins 726 lignes.")
            return False

        dh_horizontal = lignes[2].strip() + " " + lignes[3].strip()
        v_horizontal = [float(l.strip()) for l in lignes[4:364]]

        dh_vertical = lignes[364].strip() + " " + lignes[365].strip()
        v_vertical = [float(l.strip()) for l in lignes[366:726]]

        if len(v_horizontal) != 360 or len(v_vertical) != 360:
            messagebox.showerror("Erreur", "Chaque plan doit contenir exactement 360 valeurs.")
            return False

        offset_h = -max(v_horizontal) if max(v_horizontal) != 0 else 0
        offset_v = -max(v_vertical) if max(v_vertical) != 0 else 0

        v_horizontal = [val + offset_h for val in v_horizontal]
        v_vertical = [val + offset_v for val in v_vertical]

        date_h.config(text=f"Plan H: {dh_horizontal}")
        minl_h.config(text=f"Min H: {min(v_horizontal):.2f}")
        maxl_h.config(text=f"Max H: {max(v_horizontal):.2f}")

        date_v.config(text=f"Plan V: {dh_vertical}")
        minl_v.config(text=f"Min V: {min(v_vertical):.2f}")
        maxl_v.config(text=f"Max V: {max(v_vertical):.2f}")

        return True

    except Exception as erreur:
        messagebox.showerror("Erreur de lecture", str(erreur))
        return False

# Sélection du fichier
def choosefile():
    global file
    chemin = filedialog.askopenfilename(title="Choisir un fichier", filetypes=[("Fichiers texte", "*.atn"), ("Tous les fichiers", "*.*")])
    if chemin:
        file = chemin
        readfile(file)

# Tracé du graphe
def tracergraphe(couleur="purple", epaisseur=1.5, titre="Graphe Polaire"):
    global figure, canvas

    if not v_horizontal or not v_vertical:
        messagebox.showwarning("Données absentes", "Veuillez d'abord charger un fichier.")
        return

    if canvas:
        canvas.get_tk_widget().destroy()

    figure = plt.Figure(figsize=(6.5, 5), dpi=100)

    try:
        pas = int(step.get())
        if pas <= 0 or 360 % pas != 0:
            raise ValueError
    except:
        messagebox.showerror("Erreur", "Le pas doit être un diviseur exact de 360.")
        return

    angles = np.radians(np.arange(0, 360, pas))

    if m.get() == "2D":
        donnees = v_horizontal[::pas]
        if smooth.get():
            donnees = gaussian_filter1d(donnees, sigma=2)

        ax = figure.add_subplot(111, projection='polar')
        ax.plot(angles, donnees, color=couleur, linewidth=epaisseur)
        ax.set_title(titre)
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)

    else:
        ax = figure.add_subplot(111, projection='3d')

        theta = np.radians(np.arange(0, 360, pas))
        phi = np.radians(np.arange(0, 360, pas))
        THETA, PHI = np.meshgrid(theta, phi)

        r_h = np.array(v_horizontal[::pas])
        r_v = np.array(v_vertical[::pas])

        if smooth.get():
            r_h = gaussian_filter1d(r_h, sigma=2)
            r_v = gaussian_filter1d(r_v, sigma=2)

        R = np.outer(r_v, r_h)
        X = R * np.sin(PHI) * np.cos(THETA)
        Y = R * np.sin(PHI) * np.sin(THETA)
        Z = R * np.cos(PHI)

        ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='k', linewidth=0.1, alpha=0.9)
        ax.set_title("Graphe Polaire 3D")
        ax.view_init(**default_view)

    canvas = FigureCanvasTkAgg(figure, master=framegraph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Réinitialisation de la vue 3D
def reset_view():
    if figure:
        ax = figure.axes[0]
        ax.view_init(**default_view)
        canvas.draw()

# Enregistrement de l’image
def saveimage():
    if figure:
        chemin = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image PNG", "*.png")])
        if chemin:
            figure.savefig(chemin)
            messagebox.showinfo("Succès", "L’image a bien été enregistrée.")
    else:
        messagebox.showwarning("Erreur", "Aucun graphe à enregistrer.")

# Fenêtre de personnalisation
def personaliser():
    fen = tk.Toplevel(root)
    fen.title("Personnalisation")

    tk.Label(fen, text="Couleur (ex: red, blue)").grid(row=0, column=0)
    champ_couleur = tk.Entry(fen)
    champ_couleur.insert(0, "purple")
    champ_couleur.grid(row=0, column=1)

    tk.Label(fen, text="Épaisseur").grid(row=1, column=0)
    spin_ep = tk.Spinbox(fen, from_=0.5, to=10, increment=0.5)
    spin_ep.delete(0, "end")
    spin_ep.insert(0, "1.5")
    spin_ep.grid(row=1, column=1)

    tk.Label(fen, text="Titre").grid(row=2, column=0)
    champ_titre = tk.Entry(fen)
    champ_titre.insert(0, "Graphe Polaire")
    champ_titre.grid(row=2, column=1)

    def appliquer():
        try:
            tracergraphe(champ_couleur.get(), float(spin_ep.get()), champ_titre.get())
            fen.destroy()
        except Exception as err:
            messagebox.showerror("Erreur", str(err))

    tk.Button(fen, text="Appliquer", command=appliquer).grid(row=3, column=0, columnspan=2, pady=10)

# Interface utilisateur principale
topframe = tk.Frame(root)
topframe.pack(pady=10)

tk.Button(topframe, text="Choisir fichier", command=choosefile).grid(row=0, column=0, padx=5)
tk.Radiobutton(topframe, text="2D", variable=m, value="2D").grid(row=0, column=1)
tk.Radiobutton(topframe, text="3D", variable=m, value="3D").grid(row=0, column=2)
tk.Button(topframe, text="Tracer", command=tracergraphe).grid(row=0, column=3, padx=5)
tk.Button(topframe, text="Personnaliser", command=personaliser).grid(row=0, column=4, padx=5)
tk.Button(topframe, text="Enregistrer", command=saveimage, bg="green", fg="white").grid(row=0, column=5, padx=5)
tk.Button(topframe, text="Reset View", command=reset_view, bg="blue", fg="white").grid(row=0, column=6, padx=5)
tk.Checkbutton(topframe, text="Lissage", variable=smooth).grid(row=0, column=7, padx=5)

frameinfos = tk.Frame(root)
frameinfos.pack()

tk.Label(frameinfos, text="Pas (°)").grid(row=0, column=0)
tk.Entry(frameinfos, textvariable=step, width=5).grid(row=0, column=1)

date_h = tk.Label(frameinfos, text="Plan H: ")
date_h.grid(row=1, column=0, columnspan=2, sticky="w", padx=10)
minl_h = tk.Label(frameinfos, text="Min H: ")
minl_h.grid(row=1, column=2, padx=5)
maxl_h = tk.Label(frameinfos, text="Max H: ")
maxl_h.grid(row=1, column=3, padx=5)

date_v = tk.Label(frameinfos, text="Plan V: ")
date_v.grid(row=2, column=0, columnspan=2, sticky="w", padx=10)
minl_v = tk.Label(frameinfos, text="Min V: ")
minl_v.grid(row=2, column=2, padx=5)
maxl_v = tk.Label(frameinfos, text="Max V: ")
maxl_v.grid(row=2, column=3, padx=5)

framegraph = tk.Frame(root)
framegraph.pack(fill=tk.BOTH, expand=True)

root.mainloop()
