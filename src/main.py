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