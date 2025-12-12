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
   howmany = [0.10*buspax,0.40*buspax,0.45*buspax,0.05*buspax,0]
   howmany = [int(elem) for elem in howmany]
   return howmany[t0-train_arrival_time]
   
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
  
# === DELAY GENERATOR ===

def lcg(seed,prc=0.5):
	"""
	Génère un nombre aléatoire entre 0 et 1 à partir d'une graine (seed)
	La graine correspond à l'heure d'arrivée du train EN MINUTES
	pondérée par un pourcentage de retard (prc)
	"""
	
	# transformation sous le format HH:MM puis "conversion" numérique
	new_seed = (seed//60+ord(':')+seed%60)*prc*100
	
	# méthode LCG
	a,c,m = 1664525,1013904223,2**32
	value = (a*new_seed+c)%m
	
	# normalisation
	value /= m
	
	return value


def add_late(train_arrival_time,late_rate=0.5):
	
	# calcul de l'ajout
	excess = lcg(train_arrival_time,late_rate)
	
	# distribution
	if excess<0.88:
		return int(excess)
	elif excess<0.98:
		return 1+int((excess-0.88)*50)
	else:
		return 5+int((excess-0.98)*200)

# === EVENT MANAGEMENT ===

def clock(period,freq_train,freq_bus):
   # cadence les opérations

   # initialisations
   tps = 1 # compteur de minutes
   pax_arret = 0 # nombre de personnes attendant le bus
   trains = {} # trains arrivés et passagers en transit vers le bus
               # clés = heure d'arrivée du train
               # valeur = nombre de passagers cherchant le bus  
   late_trains = []               

   while tps<=period:
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
  
      time.sleep(1) # WARNING : Si period est très élevé, cette instruction peut causer des problèmes de latence sur la machine !
      tps+=1

   print("Simulation terminée")
