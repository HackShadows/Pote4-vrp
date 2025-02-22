from classes import Client, Flotte, Trajet
import filesIO as fio

depot, clients = fio.importer_vrp("data/data101.vrp")
nb_tot_clients = len(clients)
# print(depot[0])
# met = fio.METADONNEE_CONNUES.keys()
# data = ["MAX_QUANTITY"]
# print(fio._cherche_entête("data101.vrp", met, met))
# print(data)