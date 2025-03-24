import numpy as np 
import matplotlib.pyplot as plt
import traceback

def readCoord(filename):
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

    theta = np.radians(np.arange(1, len(radius)+1))
  
  return radius, theta

nomFichier= "CRMG2SG12019.atn"

radius, theta= readCoord(nomFichier)


def polarPlot(radius, theta):
  plt.figure(figsize=(6, 6))
  ax= plt.subplot(111, projection= 'polar')
  ax.plot(theta, radius, marker='.',markersize=1, linestyle='-', lw= 0.9)
  #line.set_linewidth(0.5)
  plt.title("Polar plot")
  plt.show()


polarPlot(radius, theta)
