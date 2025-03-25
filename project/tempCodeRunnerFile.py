# 1️⃣ Charger les données depuis un fichier texte (exemple : "data.txt")

def lire_donnees(fichier):
    with open(fichier, "r") as f:
        valeurs = [float(ligne.strip()) 
        for ligne in f.readlines()]
    return valeurs
