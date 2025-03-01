from classes import Flotte, Trajet




def intra_relocate(trajet: Trajet) -> tuple[float, tuple[int, int]]:
    """
    Calcule et renvoie un tuple avec des informations sur le trajet avec la plus courte longueur 
    après une itération de relocate.

    Paramètres
    ----------
    trajet : Trajet
        Trajet sur lequelle est appliqué l'opérateur relocate.

    Retourne
    -------
    Un tuple contant la différence de longueur entre le nouveau trajet et l'ancien, et 
    un tuple contenant la position originale et la nouvelle position du client relocalisé.
    """
    assert isinstance(trajet, Trajet)
    lg = trajet.longueur
    nb = trajet.nb_clients
    mini = trajet.longueur
    ind = None
    for i in range(nb):
        cli = trajet.retirer_client(i)
        tmp = trajet.longueur
        for j in range(nb):
            tmp2 = tmp + trajet.dist_ajouter_client(j, cli)
            #if tmp2 <= mini and j != i:
            if tmp2 < mini:
                mini = tmp2
                ind = (i, j)
        trajet.ajouter_client(i, cli)
    return (mini - lg, ind)


def inter_relocate(flotte: Flotte) -> tuple[float, tuple[tuple[int, int], tuple[int, int]]]:
    """
    Calcule et renvoie un tuple avec des informations sur la flotte avec la plus courte longueur 
    après une itération de relocate.

    Paramètres
    ----------
    flotte : Flotte
        Flotte sur laquelle est appliqué l'opérateur relocate.

    Retourne
    -------
    Un tuple contant la différence de longueur entre la nouvelle flotte et l'ancienne, et 
    un tuple de 2 tuples (indice trajet, indice client) contenant la position originale 
    et la nouvelle position du client relocalisé.
    """
    assert isinstance(flotte, Flotte)
    mini = 0
    ind = None
    trajets = flotte.trajets
    for i, t in enumerate(trajets):
        for x, t2 in enumerate(trajets):
            if x == i:
                min_tmp, ind_tmp = intra_relocate(trajets[x])
                #if ind_tmp != None and min_tmp <= mini: 
                if min_tmp < mini: 
                    ind = ((i, ind_tmp[0]), (x, ind_tmp[1]))
                    mini = min_tmp
            else:
                for j, c in enumerate(t.clients):
                    tmp = t.dist_retirer_client(j)
                    for y in range(t2.nb_clients+1):
                        tmp2 = tmp + t2.dist_ajouter_client(y, c)
                        #if tmp2 <= mini:
                        if tmp2 < mini:
                            mini = tmp2
                            ind = ((i, j), (x, y))
    return (mini, ind)



def intra_exchange(trajet: Trajet) -> tuple[float, tuple[int, int]]:
    """
    Calcule et renvoie un tuple avec des informations sur le trajet avec la plus courte longueur 
    après une itération de exchange.

    Paramètres
    ----------
    trajet : Trajet
        Trajet sur lequelle est appliqué l'opérateur exchange.

    Retourne
    -------
    Un tuple contant la différence de longueur entre le nouveau trajet et l'ancien, 
    et un tuple contenant les positions des clients échangés.
    """
    assert isinstance(trajet, Trajet)
    lg = trajet.longueur
    nb = trajet.nb_clients
    mini = trajet.longueur
    ind = None
    for i in range(nb):
        cli = trajet.retirer_client(i)
        for j in range(i+1, nb):
            trajet.ajouter_client(i, trajet.clients[j-1])
            tmp = trajet.longueur + trajet.dist_remplacer_client(j, cli)
            #if tmp <= mini and j != i:
            if tmp < mini:
                mini = tmp
                ind = (i, j)
            trajet.retirer_client(i)
        trajet.ajouter_client(i, cli)
    return (mini - lg, ind)


def inter_exchange(flotte: Flotte) -> tuple[float, tuple[tuple[int, int], tuple[int, int]]]:
    """
    Calcule et renvoie un tuple avec des informations sur la flotte avec la plus courte longueur 
    après une itération de exchange.

    Paramètres
    ----------
    flotte : Flotte
        Flotte sur laquelle est appliqué l'opérateur exchange.

    Retourne
    -------
    Un tuple contant la différence de longueur entre la nouvelle flotte et l'ancienne, et 
    un tuple de 2 tuples (indice trajet, indice client) contenant les positions des clients échangés.
    """
    assert isinstance(flotte, Flotte)
    mini = 0
    ind = None
    trajets = flotte.trajets
    for i, t in enumerate(trajets):
        for x, t2 in enumerate(trajets[i:]):
            if x == i:
                min_tmp, ind_tmp = intra_exchange(trajets[x])
                #if ind_tmp != None and min_tmp <= mini: 
                if min_tmp < mini: 
                    ind = ((i, ind_tmp[0]), (x, ind_tmp[1]))
                    mini = min_tmp
            else:
                for j, c in enumerate(t.clients):
                    for y, c2 in enumerate(t2.clients):
                        tmp = t.dist_remplacer_client(j, c2) + t2.dist_remplacer_client(y, c)
                        #if tmp <= mini:
                        if tmp < mini:
                            mini = tmp
                            ind = ((i, j), (x, y))
    return (mini, ind)



def effectuer_changements(flotte: Flotte, new_dist: float, indice: tuple[tuple[int, int], tuple[int, int]], action: int):
    """
    Calcule et renvoie un tuple avec des informations sur la flotte avec la plus courte longueur 
    après une itération de exchange.

    Paramètres
    ----------
    flotte : Flotte
        Flotte sur laquelle est appliqué le changement 'action'.
    new_dist : float
        Différence de distance entre avant et après le changement.
    indice : tuple[tuple[int, int], tuple[int, int]]
        Indices des deux positions sur lesquelles le changements est effectué.
    action : int
        Opérateur utilisé pour le changement (1 = relocate, 2 = exchange).
    """
    (i, j), (x, y) = indice
    trajets = flotte.trajets
    flotte.longueur += new_dist
    match action:
        case 1:
            cli = trajets[i].retirer_client(j)
            trajets[x].ajouter_client(y, cli)
        case 2:
            cli = trajets[i].clients[j]
            cli2 = trajets[x].retirer_client(y)
            trajets[x].ajouter_client(y, cli)
            trajets[i].retirer_client(j)
            trajets[i].ajouter_client(j, cli2)
