# sur GitHub, le fichier s'appelle "project.py"
# donc, dans mon nouveau fichier, je fais :
from project import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

# === GLOBAL VARIABLES ===
tps = 1 # compteur de minutes
pax_arrets = [0,0] # nombre de personnes attendant le bus
nb_arrets = len(pax_arrets)
trains = {} # trains arrivés et passagers en transit vers le bus
            # clés = heure d'arrivée du train
            # valeur = nombre de passagers cherchant le bus
late_trains = []
savings = [[] for _ in range(nb_arrets)]
# pour tkinter
app = None
fig = None
ax = None
graph = None
canvas = None
line = None
frame = None
launch_button = None
parameters = {key:None for key in [
                                    'period_label','period_input','freqtrain_label','freqtrain_input',
                                    'freqbus_label','freqbus_input','seats_label','seats_input',
                                    'stand_label','stand_input','late_label','late_input'
                                  ]
            }
text_to_display = {
    'period_label':'Durée de la simulation',
    'freqtrain_label':'Fréquence (train)',
    'freqbus_label':'Fréquence (bus)',
    'seats_label':"Nombre de places assises (bus)",
    'stand_label':'Nombre de "places debout" (bus)',
    'late_label':'Taux de retard'
}

# === EVENT MANAGEMENT ===

def clock(values):
   global tps,pax_arrets,savings,trains,late_trains
   global app,ax,graph,line

   def step():
       global tps,pax_arrets,savings,trains,late_trains
       global app,ax,graph,line
       nonlocal values
       
       # pour éviter de tout modifier (faut avoir la flemme parfois ;)
       period = int(values['period_input'])
       freq_train = int(values['freqtrain_input'])
       freq_bus = int(values['freqbus_input'])
       
       # pour les nouvelles valeurs
       seats = int(values['seats_input'])
       stand_capacity = int(values['stand_input'])
       late_rate = float(values['late_input'])

       if tps<=period:
          if tps%freq_train==0:
            delay = add_late(tps,late_rate)
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
                repartition = allocate(j,nb_arrets)
                for i in range(len(repartition)): # ajout arrêt par arrêt
                    pax_arrets[i] += repartition[i]

          if tps%freq_bus==0:
              for i in range(nb_arrets):
                gone, no_more_seats = bus_departure(pax_arrets[i],seats,stand_capacity)
                pax_arrets[i] -= gone

          # enregistre les informations
          for i in range(nb_arrets):
              savings[i].append((tps,pax_arrets[i]))
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
   
   
def reset():
    global tps,pax_arret,trains,late_trains,savings
    global ax,line
    
    # supprime l'ancien graphe
    ax.cla()
    line = ax.plot([],[],'r.-')[0]
    
    # remet les paramètres à zéro
    tps = 1
    pax_arret = 0
    trains = {}
    late_trains = []
    savings = []
    

def launch():
    global parameters
    # reset
    reset()
    
    # dictionnaire qui contient les valeurs récupérées
    values = {}
    
    for key,val in parameters.items():
        # on garde uniquement les Entry
        if "input" in key:
            user_input = val.get() # récupère la valeur
            
            # cas de late_rate
            if key=='late_input':
                if set(user_input).issubset(set('0123456789.')) and user_input!='' and 0<=float(user_input)<=1:
                    values[key] = user_input
                else:
                    values[key] = 0.5 # valeur par défaut
   
            # autres cas
            else:
                if set(user_input).issubset(set('0123456789')) and user_input!='' and int(user_input)>0:
                    values[key] = user_input
                else:
                    # vérifie si ce n'est pas 0 pour les places
                    if (key=='seats_input' or key=='stand_input') and user_input!='' and set(user_input)=={0}:
                        values[key] = user_input
                    # sinon, c'est que ce n'est pas bon !
                    else:
                        values[key] = 50 # valeur par défaut
    
    # lance la simulation
    clock(values)
    
def initialisation():
    # initialise l'interface graphique
    
    global app,fig,ax,graph,frame,canvas,line,launch_button
    global parameters,text_to_display
   
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
       
       # créer un espace user-friendly
       frame = tk.Frame(app)
       frame.grid(row=0, column=1)
       
       # construire les Label et les Entry
       i=1
       for key in parameters.keys():
           if "label" in key: # c'est un Label
               t = tk.Label(frame,text=text_to_display[key],font=('Arial',12),foreground='black')
               t.grid(row=i,column=2)
               parameters[key] = t # sauvegarde
           if "input" in key: # c'est un Entry
               t = tk.Entry(frame,relief='sunken',borderwidth=2,background='#282828',foreground='white')
               t.grid(row=i,column=3)
               i+=1
               parameters[key] = t # sauvegarde
         
       # construire le bouton
       launch_button = tk.Button(frame,text="Lancer la simulation", font=('Arial',12),relief='raised',command=launch)
       launch_button.grid(row=i,column=2)

    # lance la boucle
    app.mainloop()
    
    
# appel 
initialisation()
