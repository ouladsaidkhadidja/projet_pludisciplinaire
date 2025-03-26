import numpy as np 

import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import traceback

def readCoord(filename, step):
    radius = []
    with open(filename, 'r') as file:
        for i, line in enumerate(file):
            try:
                value = float(line.strip())
                radius.append(value)
            except ValueError:
                continue
    
    if radius:
        maxv = max(radius)
        if maxv != 0:
            radius = [r + abs(maxv) for r in radius]
    
    indices = np.arange(0, len(radius), step)  # Sélectionner avc l'incrémentation choisie
    radius = [radius[i] for i in indices]  # Filtrer les valeurs 
    theta = np.radians(indices + 1)  # Ajuster theta pour correspondre aux indices
    
    return radius, theta


step_choice = 1  # Valeur par défaut

#buttom

def onb1(event):
    updateplot(1)

def onb5(event):
    updateplot(5)
nomFichier = "C:\\Users\\Thinkpad T490\\Downloads\\CRMG1SG12019 (1).atn"
def updateplot(step):
    global step_choice
    step_choice = step
    radius, theta = readCoord(nomFichier, step_choice)
    ax.clear()
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.plot(theta, radius, marker='.', markersize=1, linestyle='-', lw=0.9)
    plt.title("Polar plot")
    plt.draw()

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
plt.subplots_adjust(bottom=0.2)
updateplot(step_choice)

ax1 = plt.axes([0.3, 0.05, 0.1, 0.075])
ax5 = plt.axes([0.6, 0.05, 0.1, 0.075])

but1 = Button(ax1, '1°')
but5 = Button(ax5, '5°')

but1.on_clicked(onb1)
but5.on_clicked(onb5)

plt.show()
