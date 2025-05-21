import tkinter as tk
from tkinter import filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import datetime
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from scipy.ndimage import gaussian_filter1d

# frame principale
# f principale
root = tk.Tk()
step = tk.StringVar(value="1")
root.title("Affichage de Graphe Polaire")
root.geometry("700x500")



# Left: control panel
#control_panel = tk.Frame(mainframe, width=200, bg="#f0f0f0")
#control_panel.pack(side=tk.LEFT, fill=tk.Y)

# Right: display panel 
#display_panel = tk.Frame(mainframe)
#display_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# les variables 

step = tk.StringVar(value="1")
file = "" #chemin du fichier
v = []   #les valeurs
dh = ""  #la date et l'heure
figure = None
canvas = None
m = tk.StringVar(value="2D") #mode

# les fonctions
def readfile(fichier): 
    global dh, v
    try:
        with open(fichier, "r") as f:
            l = f.readlines()
            if len(l) < 364:
                messagebox.showerror("Erreur", "Le fichier ne contient pas assez de l.")
                return False

            date = l[2].strip()
            heure = l[3].strip()
            dh = f"{date} {heure}"

            # read the 360 vals
            v = [float(l.strip()) for l in l[4:364]]

            if len(v) != 360:
                messagebox.showerror("Error", "Il faut exactement 360 valeurs.")
                return False

            return True
    except Exception as e:
        messagebox.showerror("Reading errror", str(e))
        return False
    
def choosefile():
    global file
    fichier = filedialog.askopenfilename(
        title="Choisir fichier",
        filetypes=[("files texte", "*.atn"), ("Tous les files", "*.*")]
    )
    if fichier:
        file = fichier
        if readfile(file):
            # save the original vals
            minval = min(v)
            maxval = max(v)

            #  decalage ida max<>0
            if maxval != 0:
                decalage = -maxval
                v[:] = [val + decalage for val in v]  # modifier la liste

            # affichage min et max
            date.config(text=f"Date/Heure: {dh}")
            minl.config(text=f"Min: {minval:.2f}")
            maxl.config(text=f"Max: {maxval:.2f}")

# variable global pour le default view
default_view = {"elev": 30, "azim": -60}
#variable globale pour le lissage
smooth = tk.BooleanVar(value=False)  # lissage désactivé par défaut

def tracergraphe(c="purple", ep=1.5, titre="Representation des donnees en graphe polaire"):
    global figure, canvas
    
    if not v:
        messagebox.showwarning("Warning", "Aucune donnée chargée.")
        return

    

    if figure and canvas:
        canvas.get_tk_widget().destroy()

    figure = plt.Figure(figsize=(6, 5), dpi=100)
    try:
        step_val = int(step.get())
        if step_val <= 0 or 360 % step_val != 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "The step should be a divisor of 360 (ex: 1, 5, 10...)")
        return

    angles = np.radians(np.arange(0, 360, step_val))
    valeurs = v[::step_val]

    if m.get() == "2D":
        ax = figure.add_subplot(111, projection='polar')

        #lissage
        if smooth.get():
            from scipy.ndimage import gaussian_filter1d
            valeurs = gaussian_filter1d(valeurs, sigma=2)  # Appliquer un lissage Gaussien
        

        ax.plot(angles, valeurs, color=c, linewidth=ep)
        ax.set_title("Graphe Polaire 2D")
        ax.set_theta_zero_location('N')
        ax.set_theta_direction(-1)
    else:
        ax = figure.add_subplot(111, projection='3d')
        
        # angles (azimut) et élévation
        angles_full = np.radians(np.arange(0, 360, step_val))
        theta, phi = np.meshgrid(angles_full, np.linspace(0, np.pi, 180))  # theta: (180, 360)

        # Interpolation des valeurs
        valeurs_interp = np.interp(np.degrees(angles_full), np.arange(0, 360, step_val), v[::step_val])  # (360,)

        # Répéter les valeurs pour chaque ligne (élévation) => (180, 360)
        r = np.tile(valeurs_interp, (phi.shape[0], 1))  # forme correcte : (180, 360)

        # Coordonnées cartésiennes
        X = r * np.sin(phi) * np.cos(theta)
        Y = r * np.sin(phi) * np.sin(theta)
        Z = r * np.cos(phi)

        # Tracer la surface
        ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.9, edgecolor='k', linewidth=0.1)
        ax.set_title("Graphe Polaire 3D")
        ax.view_init(elev=default_view["elev"], azim=default_view["azim"])


    canvas = FigureCanvasTkAgg(figure, master=framegraph)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)



    
def reset_view():
    if figure:
        ax = figure.axes[0]
        ax.view_init(elev=default_view["elev"], azim=default_view["azim"])
        canvas.draw()

def saveimage():
    if figure:
        file = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Image PNG", "*.png")])
        if file:
            figure.savefig(file)
            messagebox.showinfo("Succès", "Graphique sauvegardé avec succès !")
    else:
        messagebox.showwarning("Attention", "Aucun graphique à sauvegarder.")

def personaliser():
    f = tk.Toplevel(root)
    f.title("Personnaliser Graphe")

    # the color
    tk.Label(f, text="Couleur (ex: purple, red, blue...)").grid(row=0, column=0, pady=5)
    ec = tk.Entry(f)
    ec.insert(0, "purple")
    ec.grid(row=0, column=1, pady=5)

    # the width
    tk.Label(f, text="Épaisseur de la ligne").grid(row=1, column=0, pady=5)
    eep = tk.Spinbox(f, from_=0.5, to=10, increment=0.5)
    eep.delete(0, tk.END)
    eep.insert(0, "1.5")
    eep.grid(row=1, column=1, pady=5)

    # title
    tk.Label(f, text="Titre du graphe").grid(row=2, column=0, pady=5)
    etitre = tk.Entry(f)
    etitre.insert(0, "Graphe Polaire 2D")
    etitre.grid(row=2, column=1, pady=5)

    # modification button
    def appliquer_modifications():
        c = ec.get()
        ep = float(eep.get())
        titre = etitre.get()
        tracergraphe(c, ep, titre)
        f.destroy()

    apply = tk.Button(f, text="Appliquer", command=appliquer_modifications)
    apply.grid(row=3, column=0, columnspan=2, pady=10)




# vue
# vue
topframe = tk.Frame(root)
topframe.pack(padx=10)

choisir = tk.Button(topframe, text="Choisir file", command=choosefile)
choisir.grid(row=0, column=0, padx=5)

d2 = tk.Radiobutton(topframe, text="2D", var=m, val="2D")
d2.grid(row=0, column=1, padx=5)

d3 = tk.Radiobutton(topframe, text="3D", var=m, val="3D")
d3.grid(row=0, column=2, padx=5)

tracer = tk.Button(topframe, text="Tracer Graphe", command=tracergraphe)
tracer.grid(row=0, column=3, padx=5)

save = tk.Button(topframe, text="Enregistrer Image", command=saveimage, bg="green", fg="white")
save.grid(row=0, column=4, padx=5)

reset_btn = tk.Button(topframe, text="Reset View", command=reset_view, bg="blue", fg="white")
reset_btn.grid(row=0, column=6, padx=5)

perso = tk.Button(topframe, text="Personnaliser Graphe", command=personaliser)
perso.grid(row=0, column=5, padx=5)

frameinfos = tk.Frame(root)
frameinfos.pack(pady=5)

stepinfo = tk.Label(frameinfos, text="Pas (°)")
stepinfo.grid(row=0, column=3, padx=10)

estep = tk.Entry(frameinfos, textvar=step, width=5)
estep.grid(row=0, column=4, padx=5)

check_smooth = tk.Checkbutton(topframe, text="Lissage", variable=smooth)
check_smooth.grid(row=0, column=7, padx=5)

date = tk.Label(frameinfos, text="Date/Heure: ")
date.grid(row=0, column=0, padx=10)

minl = tk.Label(frameinfos, text="Min: ")
minl.grid(row=0, column=1, padx=10)

maxl = tk.Label(frameinfos, text="Max: ")
maxl.grid(row=0, column=2, padx=10)


framegraph = tk.Frame(root)
framegraph.pack(fill=tk.BOTH, expand=True)

# GO
root.mainloop()