from classes import Flotte
from opérateurs import inter_exchange, inter_relocate, effectuer_changements
import matplotlib.pyplot as plt
import numpy as np
import time as t
from matplotlib.animation import FuncAnimation
from random import randint



def affichage_graphique(pos_depot: tuple[int, int], pos_clients: list[tuple[int, int]], flotte: Flotte, detail: bool = False):
    t0 = t.time()
    if detail: flotte.afficher(True)
    points = np.array(pos_clients)
    lg = round(flotte.longueur, 2)
    
    # Créer la figure et les axes
    fig, ax = plt.subplots()
    pos_x, pos_y = points[:, 0], points[:, 1]
    ax.set_xlim(0, max(pos_x)+5)
    ax.set_ylim(0, max(pos_y)+8)

    # Points fixes
    ax.scatter(pos_x, pos_y, color='blue', label="Clients")
    ax.scatter(pos_depot[0], pos_depot[1], color='red', label="Dépôt")

    text_it = plt.text(2, max(pos_y)+2, "Itérations = 0")
    text_lg = plt.text(2, max(pos_y)+5, "Longueur = km")
    text_nb = plt.text(max(pos_x)-20, max(pos_y)+5, "Nombre de camions : ")

    # Stocker les lignes tracées
    #lines = [ax.plot([], [], color=f'#{(1 if (i+1)%2 else 0)*randint(((255 if (i+1)%3 else 0)), 255):02x}{(1 if (i+1)%3 else 0)*randint(((255 if (i+1)%4 else 0)), 255):02x}{(1 if (i+1)%4 else 0)*randint(((255 if (i+1)%5 else 0)), 255):02x}', linewidth=2)[0] for i in range(3)]
    lines = [ax.plot([], [], color=f'#{randint(0, 255):02x}{randint(0, 255):02x}{randint(0, 255):02x}', linewidth=2)[0] for _ in range(flotte.nb_trajets)]
    def update(frame):
        """ Met à jour toutes les lignes en même temps """

        text_it.set_text("Itérations = " + str(frame))
        text_lg.set_text(f"Longueur = {round(flotte.longueur)}km")
        text_nb.set_text(f"Nombre de camions : {flotte.nb_trajets}")

        exchange = inter_exchange(flotte)
        relocate = inter_relocate(flotte)
        if exchange[1] == None:
            if relocate[1] == None: ani.event_source.stop()
            else: effectuer_changements(flotte, relocate[0], relocate[1], 1)
        elif relocate[1] == None: effectuer_changements(flotte, exchange[0], exchange[1], 2)
        else:
            if relocate[0] < exchange[0]: effectuer_changements(flotte, relocate[0], relocate[1], 1) 
            else: effectuer_changements(flotte, exchange[0], exchange[1], 2)

        trajets = flotte.trajets
        for i, line in enumerate(lines):
            if i < flotte.nb_trajets:
                pos_cli = np.array([pos_depot] + [cli.pos for cli in trajets[i].clients] + [pos_depot])
                line.set_data(pos_cli[:,0], pos_cli[:,1])  # Mise à jour progressive
            else:
                line.set_data([], [])  # Mise à jour progressive
        

        return [text_it, text_lg, text_nb] + lines  # Retourne la liste des lignes mises à jour

    # Création de l'animation
    ani = FuncAnimation(fig, update, frames=1000, interval=20, blit=True, repeat=False)

    plt.legend()
    plt.show()

    print(f"\nLongueur initiale : {lg}km")
    print(f"Longueur finale : {round(flotte.longueur, 2)}km\n")

    if detail: flotte.afficher(True)

    t1 = t.time() - t0
    print("\nTemps d'éxecution : ", end="")
    if t1 < 1: print(round(t1*1000), "ms")
    else: print(round(t1, 2), "s")




def affichage_console(flotte: Flotte, detail: bool = False):
    t0 = t.time()
    if detail: flotte.afficher(True)
    it = 0
    continuer = True
    lg = round(flotte.longueur, 2)

    while continuer and it < 200:
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
    
    print(f"\nLongueur initiale : {lg}km")
    print(f"Longueur finale : {round(flotte.longueur, 2)}km\n")

    if detail: flotte.afficher(True)
    
    print(f"\n{it} itérations")
    print("Temps d'éxecution : ", end="")
    if t.time() - t0 < 1: print(round((t.time() - t0)*1000), "ms")
    else: print(round(t.time() - t0, 2), "s")