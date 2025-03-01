from classes import Client, Flotte, Trajet, distance
from opérateurs import inter_relocate, intra_relocate, effectuer_changements
import filesIO as fio
import time as t
from random import randint

t0 = t.time()

depot, clients = fio.importer_vrp("data/data101.vrp")
nb_tot_clients = len(clients)
trajet = Trajet(depot[0])
# print(trajet)
for i in range(nb_tot_clients):
    trajet.ajouter_client(i, clients[i])
    # print(trajet)
# print(depot[0])
# met = fio.METADONNEE_CONNUES.keys()
# data = ["MAX_QUANTITY"]
# print(fio._cherche_entête("data101.vrp", met, met))
# print(data)

d0 = Client(0, (0, 0))
c1 = Client(1, (0, 1))
c2 = Client(2, (0, 2))
c3 = Client(3, (0, 3))
c4 = Client(4, (0, 4))
c5 = Client(5, (1, 0))
c6 = Client(6, (2, 0))
c7 = Client(7, (3, 0))
c8 = Client(8, (4, 0))

trajet = Trajet(d0)
trajet2 = Trajet(d0)
# print(trajet)
# print(trajet.dist_ajouter_client(10, c1))
trajet.ajouter_client(10, c1)
# print(trajet)
# print(trajet.dist_ajouter_client(10, c3))
trajet2.ajouter_client(10, c3)
# print(trajet)
# print(trajet.dist_ajouter_client(10, c2))
trajet.ajouter_client(10, c2)
# print(trajet)
# print(trajet.dist_ajouter_client(10, c4))
trajet.ajouter_client(10, c4)

trajet2.ajouter_client(10, c5)
trajet2.ajouter_client(10, c6)
trajet2.ajouter_client(10, c7)
trajet2.ajouter_client(10, c8)

# trajet.afficher()
# trajet2.afficher()

print(round((t.time() - t0)*1000), "ms")

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


flotte = Flotte()
flotte.ajouter_camion(trajet)
flotte.ajouter_camion(trajet2)
flotte.afficher()
print()
dist, ind = inter_relocate(flotte)
effectuer_changements(flotte, dist, ind)
flotte.afficher()

print(round((t.time() - t0)*1000), "ms")


def relocate_trajet(trajet: Trajet) -> Trajet:
    """
    Modifie aléatoirement la position d'un client dans le trajet.

    Paramètres
    ----------
    trajet : Trajet
        Trajet de livraison d'un camion avec au moins 2 clients

    Retourne
    -------
    Le trajet le plus court entre celui passé en paramètre et le nouveau

    Raises
    ------
    ValueError
        Mauvaise saisie du trajet.
    """
    try:
        assert type(trajet) == Trajet and trajet.nb_clients > 1
        long = trajet.longueur
        nb = trajet.nb_clients
        ind = randint(0, nb-1)
        ind2 = randint(0, nb-1)

        while ind2 == ind : ind2 = randint(0, nb-1)
        trajet.ajouter_client(ind2, trajet.retirer_client(ind))
        # print(trajet)
        if trajet.longueur > long: trajet.ajouter_client(ind, trajet.retirer_client(ind2))
        return trajet

    except AssertionError:
        raise ValueError ("Il faut passer un trajet de type Trajet en paramètre !")

# i = 0
# it = 0
# print(trajet)
# l1 = round(trajet.longueur, 2)
# # print("\n")
# while i < 500 and it < 500000:
#     lg = trajet.longueur
#     relocate_trajet(trajet)
#     if trajet.longueur < lg: 
#         # print(trajet)
#         i = 0
#     i+=1
#     it += 1

# print(f"Longueur initiale : {l1}km")
# print(f"Longueur finale : {round(trajet.longueur, 2)}km")
# print(f"{it} itérations")