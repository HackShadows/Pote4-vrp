from classes import Flotte, Trajet
from affichage import affichage_console, affichage_graphique
import filesIO as fio


def approximation_solution(fichier: str, affichage: int = 1):
    """
    Calcule et affiche un itinéraire de livraison proche de l'optimal.

    Paramètres
    ----------
    fichier : str
        Chemin du fichier vrp contenant les informations sur les clients à livrer.
        Ex : data/data101.vrp
    affichage : int
        Entier permettant de spécifier l'affichage désiré.
        Affichage console (1), Affichage graphique (2), 
        Affichage console détaillé (3), Affichage graphique détaillé (4)
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

    detail = True if affichage in [3, 4] else False

    affichage_graphique(positions, flotte, detail) if affichage in [2, 4] else affichage_console(flotte, detail)

fichiers = [101, 102, 111, 112, 201, 202, 1101, 1102, 1201, 1202]

# affichage = int(input("Affichage console (1), Affichage graphique (2), Affichage console détaillé (3), Affichage graphique détaillé (4) :\n"))
# for num in fichiers : approximation_solution(f"data/data{num}.vrp", affichage)

num = fichiers[9]
approximation_solution(f"data/data{num}.vrp", 2)