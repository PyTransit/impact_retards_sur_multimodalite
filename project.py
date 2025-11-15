from random import uniform
import numpy as np
import time

# === MODEL FUNCTIONS ===

def train_arrival():
   # modélise l'arrivée d'un train
   # renvoie le nombre de personnes descendant du train
   return int(uniform(0.03,0.15)*360)
   
def goto_bus(pax):
   # modélise les voyageurs qui vont chercher le bus
   # renvoie le nombre de voyageurs qui vont chercher le bus
   return int(uniform(0.3,0.6)*pax)

def arrive_at_bus_stop(buspax,train_arrival_time,t0):
   # modélise la marche des voyageurs cherchant le bus
   # renvoie le nombre de voyageurs qui arrivent à l'arrêt
   # à l'instant t0
   return buspax*np.exp(-(t0-train_arrival_time)**2)
   
def bus_departure(buspax,seats,stand_capacity):
   # modélise le départ d'un bus
   # renvoie le nombre de voyageurs montés dans le bus
   # et si le bus est saturé ou non
   
  no_more_seats = False
  passengers = 0
  
  # ceux qui peuvent montent
  if buspax<=(seats+stand_capacity):
      passengers = buspax
  else:
      passengers = seats+stand_capacity

  # y a-t-il des places debout ?
  if passengers>seats:
      no_more_seats = True

  return (passengers,no_more_seats)

# === EVENT MANAGEMENT ===

def clock(period,freq_train,freq_bus):
   # cadence les opérations

   # initialisations
   tps = 1 # compteur de minutes
   pax_arret = 0 # nombre de personnes attendant le bus
   trains = {} # trains arrivés et passagers en transit vers le bus
               # clés = heure d'arrivée du train
               # valeur = nombre de passagers cherchant le bus   

   while tps<=period:
      if tps%freq_train==0:
          trains[tps] = goto_bus(train_arrival())

      for arrival,transit_pax in trains.copy().items():
          j = arrive_at_bus_stop(transit_pax,arrival,tps)
          if j==0: # nettoyer le dictionnaire en enlevant les trop bas
             del trains[arrival]
          else:
             pax_arret += j

      if tps%freq_bus==0:
          gone, no_more_seats = bus_departure(pax_arret,22,64)
          pax_arret -= gone
  
      time.sleep(1) # WARNING : Si period est très élevé, cette instruction peut causer des problèmes de latence sur la machine !
      tps+=1

   print("Simulation terminée")
