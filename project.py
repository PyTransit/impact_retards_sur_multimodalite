from random import uniform
import numpy as np

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
