from classes import Flotte, Trajet
from affichage import affichage_console, affichage_graphique
import filesIO as fio


def approximation_solution(fichier: str):
    """
    Calcule et affiche un itinéraire de livraison proche de l'optimal.

    Paramètres
    ----------
    fichier : str
        Chemin du fichier vrp contenant les informations sur les clients à livrer.
        Ex : data/data101.vrp
    """

    depot, clients = fio.importer_vrp(fichier)

    positions = [cli.pos for cli in clients]

    trajet = Trajet(depot[0])
    flotte = Flotte(200)
    
    for i, cli in enumerate(clients):
        if trajet.marchandise > flotte.capacite / 2:
            flotte.ajouter_trajet(trajet)
            trajet = Trajet(depot[0])
        trajet.ajouter_client(i, cli)
    flotte.ajouter_trajet(trajet)

    choix = int(input("Affichage console (1), Affichage graphique (2), Affichage console détaillé (3), Affichage graphique détaillé (4) :\n"))
    detail = True if choix in [3, 4] else False

    affichage_graphique(positions, flotte, detail) if choix in [2, 4] else affichage_console(flotte, detail)


approximation_solution("data/data101.vrp")





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
# flotte = Flotte()
# flotte.ajouter_trajet(trajet)
# flotte.ajouter_camion(trajet2)
# flotte.afficher()
# print(inter_exchange(flotte))
# dist, ind = inter_exchange(flotte)
# effectuer_changements(flotte, dist, ind, 2)
# flotte.afficher()

