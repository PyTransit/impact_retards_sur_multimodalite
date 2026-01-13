*Ce projet est lié au PyProject n°1 [Mesurer l'impact des retards sur les connexions multimodales](https://pytransit.wordpress.com/2025/11/15/preparer-le-terrain-et-explication-de-la-theorie/)*
______________________

👉 Vous regardez actuellement le projet au stade de l'article du 15 janvier 2026
____

Le but du projet est de mesurer l’impact que peut avoir les retards des trains sur l’occupation des bus desservant une certaine gare. En particulier, on cherchera à représenter graphiquement l’évolution des passagers de lignes de bus en fonction des retards dans une interface graphique détaillée.

À quoi le projet peut-il servir ?
- À comprendre la succession d’évènements qui pousse une ligne stable à saturation,
- À développer des moyens pouvant permettre la prise de mesures pour limiter la propagation des perturbations sur d’autres lignes

## Contenu du projet
| Fichier | Contenu |
|--|--|
| ``project.py``  | contient toutes les fonctions modélisant un évènement en particulier dans notre simulation ainsi que la fonction de cadencement (détails plus loin)|
| ``tkinterface.py`` | contient toutes les fonctions permettant de construire l'interface graphique tkinter |
| ``LICENSE`` | la licence de ce projet : MIT |
| ``README.md`` | ce que vous êtes en train de lire :) |
| ``.gitignore`` | *(pour les développeurs)* |

Le fichier ``project.py`` contient
| Fonction | Ce qu'elle fait |
|--|--|
| ``train_arrival()`` | Renvoie le nombre de passagers descendant d'un train à quai |
| ``goto_bus(pax)`` | Renvoie le nombre de passagers descendus souhaitant prendre le bus. ``pax`` est le résultat de ``train_arrival()``|
| ``arrive_at_bus_stop(buspax,train_arrival_time,t0)``| Simule l'arrivée progressive des passagers à un arrêt de bus. Elle renvoie le nombre de personnes issues du train arrivé à ``train_arrival_time`` et venant d'arriver à l'arrêt à ``t0``. |
| ``bus_departure(buspax,seats,stand_capacity)`` | Renvoie <ul><li>le nombre de passagers montés dans un bus ayant ``seats`` places assises et ``stand_capacity`` places "debout"</li><li>un booléen indiquant si toutes les places assises sont occupées</li></ul> ``buspax`` correspond au nombre de passagers en attente à l'arrêt. |
| ``lcg(seed,prc=0.5)`` | Renvoie un nombre aléatoire compris entre 0 et 1 et qui va déterminer si le train arrivé à ``seed`` minutes sera en retard ou non. ``prc`` n'est pas utilisé dans cette version. |
| ``add_late(train_arrival_time,late_rate=0.5)`` | Renvoie un temps supplémentaire au train censé arrivé à ``train_arrival_time``. ``late_rate`` n'est pas utilisé dans cette version. |

Le fichier ``tkinterface.py`` contient 
| Fonction | Ce qu'elle fait |
|--|--|
| lignes 9 à 22 | des variables globales permettant de stocker l'interface graphique entière ou une partie, ainsi que les variables de la simulation (``tps``, ``trains``,...) |
| ``clock(period,freq_train,freq_bus)`` | <ul><li>Construit et actualise le graphique sur l'interface graphique tkinter</li><li>Lance et arrête la simulation au bout de ``period`` secondes. ``freq_train`` et ``freq_bus`` sont les intervalles constants séparant deux arrivées successives de trains/de bus. Prend désormais en compte les retards. Cette partie est gérée par la sous-fonction ``step()``</li></ul> |

## Lancer le projet

Au stade actuel, le projet ne fonctionne pas tout seul. Il faut (après avoir téléchargé le code source) effectuer un appel à la fonction ``clock()``. \
Il n'est désormais **plus nécessaire** d'ajouter des ``print()`` : un simple appel à ``clock()`` va construire la fenêtre graphique où sera affiché le graphique représentant l'évolution.

## Liens

Accéder aux articles du PyProject : [PyProject #1 (lien vers le blog)](https://pytransit.wordpress.com/pyproject-mesurer-limpact-des-retards-sur-les-connexions-multimodales/)\
Accéder aux versions précédentes :
- [version du 15 novembre 2025 (corrigée)](https://github.com/PyTransit/impact_retards_sur_multimodalite/releases/tag/corr_exp)
- [version du 15 décembre 2025](https://github.com/PyTransit/impact_retards_sur_multimodalite/releases/tag/15dec2025)
  
Télécharger le dossier code source (y compris anciennes versions): [Releases (GitHub)](https://github.com/PyTransit/impact_retards_sur_multimodalite/releases) 
