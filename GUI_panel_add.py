import numpy as np 
import matplotlib.pyplot as plt
import traceback

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
from mpl_toolkits.mplot3d import Axes3D  # important for 3D
import re

root = tk.Tk()
root.geometry("1200x700")

root.columnconfigure(0, weight=1)  # left panel (small weight)
root.columnconfigure(1, weight=4)  # right panel (big weight)
root.rowconfigure(0, weight=1)

# Left panel
control_frame = tk.Frame(root, bg="lightgray", width=300)
control_frame.grid(row=0, column=0, sticky="nswe")  # fill North/South/West/East

# Right panel
plot_frame = tk.Frame(root, bg="white")
plot_frame.grid(row=0, column=1, sticky="nswe")  # fill fully

#3d option

#is_3d = tk.BooleanVar()

# Create one StringVar to hold the selected option
plot_mode = tk.StringVar(value="2D")  # default to 2D

#coisir le step de degree
# Variable pour stocker le pas choisi
degree_step_var = tk.StringVar(value="1")  # valeur par défaut: 1°

def readCoord(filename, step):
 
  radius=[]
  #theta1=[]
  with open(filename, 'r') as file:
    for i, line in enumerate(file):
      
      try:
        value= float(line.strip())
        try:
          radius.append(value)
        except Exception:
          print(traceback.format_exc())
      except ValueError:
        continue
    
    maxv= max(radius)
    if max(radius)!= 0:
      radius=[r+ abs(maxv) for r in radius]

    theta = np.radians(np.arange(step, step * len(radius) + 1, step))
    #if len(radius) == 360 :
    #theta = np.radians(np.arange(1, len(radius)+1))
    #elif  autreDegre  :
    #theta = np.radians(np.arange(5, 5 * len(radius) + 1, 5))
    #theta = np.radians(np.arange(autreDegre, autreDegre * len(radius) + 1, autreDegre)) #???
    #else:
      #raise ValueError(f"Nombre de valeurs inattendu : {len(radius)}. Attendu 360 ou 72.")

  
    return radius, theta

#nomFichier= "CRMG2SG12019.atn"

#radius, theta= readCoord(nomFichier)


def polarPlot(radius, theta, date_str="", time_str=""):
  fig = plt.figure(figsize=(6, 6))
  ax= fig.add_subplot(111, projection= 'polar')
  ax.plot(theta, radius, marker='.',markersize=1, linestyle='-', lw= 0.9)
  ax.set_theta_zero_location("N")
  ax.set_theta_direction(-1)
  #line.set_linewidth(0.5)
  
  title_str = "Polar plot"
  #to add date and time if provided in the given file
  if date_str or time_str:
      title_str += f"\n{date_str} {time_str}"

  fig.suptitle(title_str, fontsize=12)
  
  #plt.show()
  return fig

def polarPlot3D(radius, theta):
    fig = plt.figure(figsize=(7,7))
    ax = fig.add_subplot(111, projection='3d')

    # Create Z-axis (fake height)
    z = np.zeros_like(theta)

    # Plot in 3D
    ax.plot(radius * np.cos(theta), radius * np.sin(theta), z, lw=2)

    ax.set_title("3D Polar Plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    
    return fig

current_figure = None

def open_file():
    global current_figure
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            step = int(degree_step_var.get())  # get the user input
            if step <= 0:
                raise ValueError
        except ValueError:
            print("Invalid step size, must be positive integer.")
            return
        
        radius, theta = readCoord(file_path, step)
        date_str, time_str = get_date_time(file_path)
        #fig = polarPlot(radius, theta)

        # Update the labels
        date_label.config(text=f"Date: {date_str or 'not found'}")
        time_label.config(text=f"Time: {time_str or 'not found'}")

        for widget in plot_frame.winfo_children():
            widget.destroy()
        
        # Create the figure based on user's choice
        if plot_mode.get() == "2D":
            fig = polarPlot(radius, theta, date_str, time_str)
        elif plot_mode.get() == "3D":
            fig = polarPlot3D(radius, theta)
        else:
            print("No plot type selected.")

        current_figure = fig  # stocke la figure actuelle
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()


def save_plot():
    if current_figure is None:
        print("No figure to save!")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png")])
    if file_path:
        current_figure.savefig(file_path)
        print(f"Plot saved as {file_path}")


#getting the date and hour



def get_date_time(filename):
    date_pattern = re.compile(r'\d{2}-\d{2}-\d{4}')  # YYYY-MM-DD
    time_pattern = re.compile(r'\d{2}:\d{2}(:\d{2})?')  # HH:MM or HH:MM:SS

    date_str = ""
    time_str = ""
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not date_str and date_pattern.match(line):
                date_str = line
            elif not time_str and time_pattern.match(line):
                time_str = line

            # If both found, we can stop early
            if date_str and time_str:
                break

    return date_str, time_str



#polarPlot(radius, theta)

load_btn = tk.Button(control_frame, text="Load Data File", command=open_file)
load_btn.pack(pady=20)

# Label + Entry
#tk.Label(control_frame, text="Degree step:").pack(pady=5)
#degree_step_entry = tk.Entry(control_frame, textvariable=degree_step_var)
#degree_step_entry.pack(pady=5)

# Crée un sous-frame pour aligner horizontalement
step_frame = tk.Frame(control_frame)
step_frame.pack(pady=5)

# Label aligné à gauche
tk.Label(step_frame, text="Degree step:").pack(side="left")

# Champ Entry aligné à droite
degree_step_entry = tk.Entry(step_frame, textvariable=degree_step_var, width=5)
degree_step_entry.pack(side="left")

# Create RadioButtons
radio_2d = tk.Radiobutton(control_frame, text="2D Plot", variable=plot_mode, value="2D")
radio_2d.pack(pady=5)

radio_3d = tk.Radiobutton(control_frame, text="3D Plot", variable=plot_mode, value="3D")
radio_3d.pack(pady=5)

#date and time display
date_label = tk.Label(control_frame, text="Date: not found", anchor="w")
date_label.pack(fill="x", pady=2)

time_label = tk.Label(control_frame, text="Time: not found", anchor="w")
time_label.pack(fill="x", pady=2)

# save figuer button
save_btn = tk.Button(control_frame, text="Enregistrer le graph", command=save_plot, bg="blue", fg="white")
save_btn.pack(pady=10)


root.mainloop()  