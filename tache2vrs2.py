import numpy as np 
import matplotlib.pyplot as plt
import traceback
from matplotlib.widgets import Button

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
    
    indices = np.arange(0, len(radius), step)  # Sélectionner les indices avec l'incrémentation choisie
    radius = [radius[i] for i in indices]  # Filtrer les valeurs de radius
    theta = np.radians(indices + 1)  # Ajuster theta pour correspondre aux indices
    
    return radius, theta

nomFichier = "C:\\Users\\Thinkpad T490\\Downloads\\CRMG1SG12019 (1).atn"
step_choice = 1  # Valeur par défaut

def update_plot(step):
    global step_choice
    step_choice = step
    radius, theta = readCoord(nomFichier, step_choice)
    ax.clear()
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.plot(theta, radius, marker='.', markersize=1, linestyle='-', lw=0.9)
    plt.title("Polar plot")
    plt.draw()

def on_button_1(event):
    update_plot(1)

def on_button_5(event):
    update_plot(5)

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})
plt.subplots_adjust(bottom=0.2)
update_plot(step_choice)

ax_button_1 = plt.axes([0.3, 0.05, 0.1, 0.075])
ax_button_5 = plt.axes([0.6, 0.05, 0.1, 0.075])

button_1 = Button(ax_button_1, '1°')
button_5 = Button(ax_button_5, '5°')

button_1.on_clicked(on_button_1)
button_5.on_clicked(on_button_5)

plt.show()
