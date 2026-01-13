# sur GitHub, le fichier s'appelle "project.py"
# donc, dans mon nouveau fichier, je fais :
from project import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# === GLOBAL VARIABLES ===
tps = 1 # compteur de minutes
pax_arret = 0 # nombre de personnes attendant le bus
trains = {} # trains arrivés et passagers en transit vers le bus
            # clés = heure d'arrivée du train
            # valeur = nombre de passagers cherchant le bus
late_trains = []
savings = []
# pour tkinter
app = None
fig = None
ax = None
graph = None
canvas = None
line = None

# === EVENT MANAGEMENT ===

def clock(period,freq_train,freq_bus):
   global tps,pax_arret,savings,trains,late_trains
   global app,fig,ax,graph,canvas,line

   # initialisation
   if app is None:
       app = tk.Tk()

       # créer une figure
       fig = Figure(figsize=(4,4))
       # créer une sous-figure (notre graphique !)
       ax = fig.add_subplot(111)

       graph = FigureCanvasTkAgg(fig, master=app)
       canvas = graph.get_tk_widget()
       canvas.grid(row=0, column=0)

       line = ax.plot([],[],'r.-')[0]

   def step():
       global tps,pax_arret,savings,trains,late_trains
       global ax,graph,line
       nonlocal period,freq_train,freq_bus

       if tps<=period:
          if tps%freq_train==0:
            delay = add_late(tps)
            if delay==0:
                trains[tps] = goto_bus(train_arrival())
            else:
                late_trains.append(tps) # rappelle qu'un train en retard va arriver

          # un train en retard arrive ?
          if tps in late_trains:
            late_trains.pop(late_trains.index(tps)) # nettoyage
            trains[tps] = goto_bus(train_arrival()) # passagers arrivent

          for arrival,transit_pax in trains.copy().items():
            j = arrive_at_bus_stop(transit_pax,arrival,tps)
            if j==0: # nettoyer le dictionnaire en enlevant les trop bas
                del trains[arrival]
            else:
                pax_arret += j

          if tps%freq_bus==0:
            gone, no_more_seats = bus_departure(pax_arret,22,64)
            pax_arret -= gone

          # enregistre les informations
          savings.append((tps,pax_arret))
          # classe les informations
          times,pax = map(list,zip(*savings))

          # met à jour le graphique
          line.set_data(times,pax)
          ax.relim()
          ax.autoscale_view()
          graph.draw_idle()

          # prochaine minute
          tps+=1
          app.after(1000,step)

       else:
          print("Simulation terminée")
          return


   app.after(0,step)
   app.mainloop()
