from classes import Client, Flotte, Trajet, distance
import filesIO as fio
from random import randint

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

# d0 = Client(0, (0, 0))
# c1 = Client(1, (0, 1))
# c2 = Client(2, (0, 2))
# c3 = Client(3, (0, 3))
# c4 = Client(4, (0, 4))
# trajet = Trajet(d0)
# print(trajet)
# trajet.ajouter_client(10, c1)
# print(trajet)
# trajet.ajouter_client(10, c3)
# print(trajet)
# trajet.ajouter_client(10, c2)
# print(trajet)
# trajet.ajouter_client(10, c4)
# print(trajet)

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

i = 0
it = 0
print(trajet)
l1 = round(trajet.longueur, 2)
# print("\n")
while i < 500 and it < 500000:
    lg = trajet.longueur
    relocate_trajet(trajet)
    if trajet.longueur < lg: 
        # print(trajet)
        i = 0
    i+=1
    it += 1

print(f"Longueur initiale : {l1}km")
print(f"Longueur finale : {round(trajet.longueur, 2)}km")
print(f"{it} itérations")