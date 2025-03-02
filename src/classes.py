import math

class Client :

	__slots__ = "id", "pos", "demande", "intervalle_livraison", "temps_livraison"

	def __init__(self, id: str = "-1", pos: tuple[int, int] = (0, 0), intervalle_livraison: tuple[int, int] = (-1, -1), temps_livraison: int = 0, demande: int = 0) -> None:
		self.id = id
		self.pos = pos
		self.demande = demande
		self.intervalle_livraison = intervalle_livraison
		self.temps_livraison = temps_livraison


	def __repr__(self) -> str :
		x, y = self.pos
		return f"Client(id: {self.id}, position: ({x} {y}))"
	

	def afficher(self):
		x, y = self.pos
		début, fin = self.intervalle_livraison
		temps = self.temps_livraison
		print(f"Client(id: {self.id}, position: ({x} {y}), livraison entre {début} et {fin}, demande: {self.demande}, temps de livraison: {temps})")



def distance(client1: Client, client2: Client) -> float:
	x1, y1 = client1.pos
	x2, y2 = client2.pos
	return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)





class Trajet :

	__slots__ = "longueur", "nb_clients", "clients", "depot", "marchandise"

	def __init__(self, depot: Client = Client()):
		self.longueur = 0.0
		self.nb_clients = 0
		self.clients = []
		self.depot = depot
		self.marchandise = 0

	
	def __repr__(self) -> str:
		long = self.longueur
		nb = self.nb_clients
		return f"Trajet(longueur : {round(long, 2)}km, contient {nb} clients)"
	
	
	def afficher(self, capacite = False):
		long = self.longueur
		nb = self.nb_clients
		capa = self.marchandise
		print(f"Trajet(longueur : {round(long, 2)}km, contient {nb} clients, {capa if capacite else [e.id for e in self.clients]})")
	
	
	def ajouter_client(self, indice: int, client: Client):
		"""
		Ajoute un client à la feuille de route, à la position 'indice'.

		Paramètres
		----------
		indice : int
			Indice du client dans la liste 'clients'.
		client : Client
			Client à ajouter dans l'itinéraire de livraison.
		"""
		assert isinstance(client, Client)
		assert isinstance(indice, int) and indice >= 0
		self.longueur += self.dist_ajouter_client(indice, client)
		self.clients.insert(indice, client)
		self.nb_clients += 1
		self.marchandise += client.demande
	
	
	def retirer_client(self, indice: int) -> Client:
		"""
		Retire un client de l'itinéraire, et le renvoie.

		Paramètres
		----------
		indice : int
			Indice du client dans la liste non vide 'clients'.

		Retourne
		-------
		Le client se trouvant à l'indice passé en paramètre
		"""
		assert isinstance(indice, int) and indice < self.nb_clients and indice >= 0 and self.nb_clients > 0
		self.longueur += self.dist_retirer_client(indice)
		cli = self.clients.pop(indice)
		self.nb_clients -= 1
		self.marchandise -= cli.demande
		return cli
	
	
	def dist_ajouter_client(self, indice: int, client: Client) -> float:
		"""
		Calcule et renvoie la différence de distance entre avant et après l'ajout du client.

		Paramètres
		----------
		indice : int
			Indice du client dans la liste 'clients'.
		client : Client
			Client à ajouter dans l'itinéraire de livraison.

		Renvoie
		-------
		La différence positive de distance entre avant et après l'ajout du client
		"""
		assert isinstance(client, Client)
		assert isinstance(indice, int) and indice >= 0
		if self.nb_clients == 0: lg = 2 * distance(self.depot, client)
		else: 
			if indice == 0: lg = distance(client, self.depot) + distance(client, self.clients[0]) - distance(self.clients[0], self.depot)
			elif indice >= self.nb_clients: lg = distance(client, self.depot) + distance(client, self.clients[-1]) - distance(self.clients[-1], self.depot)
			else: lg = distance(client, self.clients[indice-1]) + distance(client, self.clients[indice]) - distance(self.clients[indice-1], self.clients[indice])
		return lg
	
	
	def dist_retirer_client(self, indice: int) -> float:
		"""
		Calcule et renvoie la différence de distance entre avant et après le retrait du client.

		Paramètres
		----------
		indice : int
			Indice du client dans la liste non vide 'clients'.

		Retourne
		-------
		La différence négative de distance entre avant et après le retrait du client
		"""
		assert isinstance(indice, int) and indice < self.nb_clients and indice >= 0 and self.nb_clients > 0
		cli = self.clients[indice]
		if self.nb_clients == 1: lg = - self.longueur
		else: 
			if indice == 0: lg = distance(self.clients[1], self.depot) - distance(cli, self.depot) - distance(cli, self.clients[1])
			elif indice == self.nb_clients - 1: lg = distance(self.clients[-2], self.depot) - distance(cli, self.depot) - distance(cli, self.clients[-2])
			else: lg = distance(self.clients[indice-1], self.clients[indice+1]) - distance(cli, self.clients[indice+1]) - distance(cli, self.clients[indice-1])
		return lg


	def dist_remplacer_client(self, indice: int, client: Client) -> float:
		"""
		Calcule et renvoie la différence de distance entre avant et après le remplacement du client.

		Paramètres
		----------
		indice : int
			Indice du client à remplacer dans la liste non vide 'clients'.
		client : Client
			Client utilisé pour le remplacement.

		Renvoie
		-------
		La différence de distance entre avant et après le remplacement du client
		"""
		assert isinstance(client, Client) and self.nb_clients > 0
		assert isinstance(indice, int) and indice >= 0 and indice < self.nb_clients
		cli = self.clients[indice]
		if self.nb_clients == 1: lg = 2 * distance(self.depot, client) - self.longueur
		else: 
			if indice == 0: lg = distance(client, self.depot) + distance(client, self.clients[1]) - distance(cli, self.depot) - distance(cli, self.clients[1])
			elif indice == self.nb_clients-1: lg = distance(client, self.depot) + distance(client, self.clients[-2]) - distance(cli, self.depot) - distance(cli, self.clients[-2])
			else: lg = distance(client, self.clients[indice-1]) + distance(client, self.clients[indice+1]) - distance(cli, self.clients[indice-1]) - distance(cli, self.clients[indice+1])
		return lg
		




class Flotte :

	__slots__ = "capacite", "longueur", "nb_trajets", "trajets"

	def __init__(self, capacite: int = 0):
		self.capacite = capacite
		self.longueur = 0.0
		self.nb_trajets = 0
		self.trajets = []
	
	
	def __repr__(self) -> str :
		long = self.longueur
		nb = self.nb_trajets
		return f"Flotte(longueur : {round(long, 2)}km, contient {nb} camions)"
	
	
	def afficher(self, capacite = False):
		print(self)
		for t in self.trajets:
			t.afficher(capacite)
		print()

	
	def ajouter_trajet(self, trajet: Trajet):
		"""
		Ajoute un itinéraire de livraison.

		Paramètres
		----------
		trajet : Trajet
			Itinéraire de livraison à ajouter.
		"""
		assert trajet.marchandise <= self.capacite
		assert isinstance(trajet, Trajet)
		self.trajets.append(trajet)
		self.longueur += trajet.longueur
		self.nb_trajets += 1
	
	
	def retirer_trajet(self, indice: int) -> Trajet:
		"""
		Retire et renvoie un itinéraire de livraison.

		Paramètres
		----------
		indice : int
			Indice de l'itinéraire dans la liste 'trajets'.

		Retourne
		-------
		L'itinéraire de livraison qui a été retiré.
		"""
		assert isinstance(indice, int) and indice < self.nb_trajets and indice >= 0
		t = self.trajets.pop(indice)
		self.longueur -= t.longueur
		self.nb_trajets -= 1
		return t
