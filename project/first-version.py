import matplotlib.pyplot as plt   # Pour le dessin du graphe
import numpy as np  #Utile pour effectuer des opérations mathématiques, notamment la conversion d'angles en radians.

# read the file
def read_file(file):
    with open(file, "r") as f:
        valeurs = [float(ligne.strip()) for ligne in f.readlines()]
    return valeurs


# dessiner le graphe
def graph(file):
    valeurs = read_file(file)

    if len(valeurs) != 360:
        print("Erreur : Il faut exactement 360 valeurs pour un graphe sur 360°")
        return
    
    angles = np.radians(np.arange(0, 360, 1))  # Convertir les angles en radians
    
    # Tracer le graphe en coordonnées polaires
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    ax.plot(angles, valeurs, linewidth=2, color="purple") 

    # decoration
    ax.set_title("Graphique en coordonnées polaires", fontsize=14)
    ax.set_theta_zero_location('N')  # 0° en haut
    ax.set_theta_direction(-1)  # Sens antihoraire

    plt.show()

# call the functions
file = r"C:\Users\DELL\Desktop\project\data.atn"
graph(file)
