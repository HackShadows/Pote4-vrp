from classes import Client, Flotte, Trajet, distance
from opérateurs import *
import filesIO as fio
import time as t

t0 = t.time()

depot, clients = fio.importer_vrp("data/data101.vrp")
nb_tot_clients = len(clients)
trajet = Trajet(depot[0])
# print(trajet)
for i in range(nb_tot_clients):
    trajet.ajouter_client(i, clients[i])
print(trajet)
# print(depot[0])
# met = fio.METADONNEE_CONNUES.keys()
# data = ["MAX_QUANTITY"]
# print(fio._cherche_entête("data101.vrp", met, met))
# print(data)

# d0 = Client(0, (0, 0))
# c1 = Client(1, (0, 1))
# c2 = Client(2, (0, 2))
# c3 = Client(3, (0, 3))
# c4 = Client(4, (0, 4))
# c5 = Client(5, (1, 0))
# c6 = Client(6, (2, 0))
# c7 = Client(7, (3, 0))
# c8 = Client(8, (4, 0))

# trajet = Trajet(d0)
# trajet2 = Trajet(d0)
# # print(trajet)
# # print(trajet.dist_ajouter_client(10, c1))
# trajet.ajouter_client(10, c1)
# # print(trajet)
# # print(trajet.dist_ajouter_client(10, c3))
# trajet.ajouter_client(10, c3)
# # print(trajet)
# # print(trajet.dist_ajouter_client(10, c2))
# trajet2.ajouter_client(10, c2)
# print(trajet)
# print(trajet.dist_ajouter_client(10, c4))
# trajet.ajouter_client(10, c4)

# trajet2.ajouter_client(0, c5)
# trajet.ajouter_client(1, c6)
# trajet2.ajouter_client(10, c7)
# trajet2.ajouter_client(10, c8)

# trajet.afficher()
# trajet2.afficher()

# print(round((t.time() - t0)*1000), "ms")

# print(trajet.dist_retirer_client(0))
# trajet.retirer_client(0)
# trajet.afficher()
# print(trajet.dist_retirer_client(0))
# trajet.retirer_client(0)
# trajet.afficher()
# print(trajet.dist_retirer_client(0))
# trajet.retirer_client(0)
# trajet.afficher()
# print(trajet.dist_retirer_client(0))
# trajet.retirer_client(0)
# print(trajet)

# print(trajet.dist_remplacer_client(2, c3))
# print(intra_exchange(trajet))
flotte = Flotte()
flotte.ajouter_camion(trajet)
# flotte.ajouter_camion(trajet2)
# flotte.afficher()
# print(inter_exchange(flotte))
# dist, ind = inter_exchange(flotte)
# effectuer_changements(flotte, dist, ind, 2)
# flotte.afficher()

def approximer_solution(flotte: Flotte) -> tuple[int, Flotte]:
    it = 0
    continuer = True

    while continuer and it < 300:
        exchange = inter_exchange(flotte)
        relocate = inter_relocate(flotte)
        if exchange[1] == None:
            if relocate[1] == None: continuer = False
            else: effectuer_changements(flotte, relocate[0], relocate[1], 1)
        elif relocate[1] == None: effectuer_changements(flotte, exchange[0], exchange[1], 2)
        else:
            if relocate[0] < exchange[0]: effectuer_changements(flotte, relocate[0], relocate[1], 1) 
            else: effectuer_changements(flotte, exchange[0], exchange[1], 2)
        it += 1
    
    return (it, flotte)


print(flotte)
t0 = t.time()
lg = round(flotte.longueur, 2)

it, flotte2 = approximer_solution(flotte)

print(f"Longueur initiale : {lg}km")
print(f"Longueur finale : {round(flotte.longueur, 2)}km")
print(f"{it} itérations")

print("Temps d'éxecution : ", end="")
if t.time() - t0 < 1: print(round((t.time() - t0)*1000), "ms")
else: print(round(t.time() - t0, 2), "s")