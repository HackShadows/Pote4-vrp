from classes import Client, Flotte, Trajet, distance

def intra_relocate(trajet: Trajet):
    lg = trajet.longueur
    mini = trajet.longueur
    ind = None
    for i in range(trajet.nb_clients):
        cli = trajet.retirer_client(i)
        tmp = trajet.longueur
        for j in range(trajet.nb_clients+1):
            tmp2 = tmp + trajet.dist_ajouter_client(j, cli)
            if tmp2 < mini:
                mini = tmp + trajet.dist_ajouter_client(j, cli)
                ind = (i, j)
        trajet.ajouter_client(i, cli)
    return mini - lg, ind

def inter_relocate(flotte: Flotte):
    mini = 0
    ind = None
    for i, t in enumerate(flotte.trajets):
        for x, t2 in enumerate(flotte.trajets):
            if x == i:
                min_tmp, ind_tmp = intra_relocate(flotte.trajets[x])
                if min_tmp < mini: 
                    ind = ((i, ind_tmp[0]), (x, ind_tmp[1]))
                    mini = min_tmp
            else:
                for j, c in enumerate(t.clients):
                    tmp = t.dist_retirer_client(j)
                    for y in range(t2.nb_clients+1):
                        tmp2 = tmp + t2.dist_ajouter_client(y, c)
                        if tmp2 < mini:
                            mini = tmp2
                            ind = ((i, j), (x, y))
    return mini, ind

def effectuer_changements(flotte: Flotte, dist: float, ind: tuple[tuple[int, int], tuple[int, int]]):
    cli = flotte.trajets[ind[0][0]].retirer_client(ind[0][1])
    flotte.trajets[ind[1][0]].ajouter_client(ind[1][1], cli)
    flotte.longueur += dist
