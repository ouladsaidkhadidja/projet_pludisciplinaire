import numpy as np
import matplotlib.pyplot as plt

def lire_fichier(nomfic):
    valeurs = []
    with open(nomfic, "r") as f:
        for ligne in f:
            elements = ligne.strip().split()  # Séparation par espace
            for e in elements:
                try:
                    valeurs.append(float(e))  
                except ValueError:
                    pass  #l ignorer si c est pas un nombre
    return np.array(valeurs)


def convertir_en_puissance_relative(valeursdb):
    Pmax = np.max(10**(valeursdb / 10))  # pmax
    return (10**(valeursdb / 10)) / Pmax  # P/Pmax

# les angles
def generer_angles(n):
    return np.linspace(0, 2 * np.pi, n)  # radian


def tracer_diagramme_polaire(angles, valeurs):
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection="polar")
    ax.plot(angles, valeurs, "b.-")  
    ax.set_title("Graphe")
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    plt.show()


#fichier = "C:\\Users\\Thinkpad T490\\OneDrive\\Bureau\\data.txt"  
fichier = "C:\\Users\\Thinkpad T490\\OneDrive\\Bureau\\t20191h.txt"
#fichier="C:\\Users\\Thinkpad T490\\OneDrive\\Bureau\\datapol.txt"
#fichier ="C:\\Users\\Thinkpad T490\\OneDrive\\Bureau\\t20192h.txt"
valeursdb = lire_fichier(fichier)  # Lire le fichier
print(valeursdb)
valeursrel = convertir_en_puissance_relative(valeursdb)  #  P/Pmax

angles = generer_angles(len(valeursdb))  


tracer_diagramme_polaire(angles, valeursrel)



