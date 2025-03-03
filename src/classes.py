from math import sqrt





class Client :

	__slots__ = "id", "pos", "demande", "intervalle_livraison", "temps_livraison"

	def __init__(self, id_ :str = "-1", pos :tuple[int, int] = (0, 0), intervalle_livraison :tuple[int, int] = (-1, -1), temps_livraison :int = 0, demande :int = 0) :
		self.id = id_
		self.pos = pos
		self.demande = demande
		self.intervalle_livraison = intervalle_livraison
		self.temps_livraison = temps_livraison


	def __repr__(self) -> str :
		x, y = self.pos
		return f"Client(id: {self.id}, position: ({x} {y}))"
	

	def afficher(self) :
		x, y = self.pos
		début, fin = self.intervalle_livraison
		temps = self.temps_livraison
		print(f"Client(id: {self.id}, position: ({x} {y}), livraison entre {début} et {fin}, demande: {self.demande}, temps de livraison: {temps})")



def distance(client1 :Client, client2 :Client) -> float :
	x1, y1 = client1.pos
	x2, y2 = client2.pos
	return sqrt((x2 - x1)**2 + (y2 - y1)**2)





class Trajet :

	__slots__ = "longueur", "nb_clients", "clients", "depot", "marchandise"

	def __init__(self, depot :Client = Client()) :
		self.longueur = 0.0
		self.nb_clients = 0
		self.clients = []
		self.depot = depot
		self.marchandise = 0


	def __repr__(self) -> str :
		long = self.longueur
		nb = self.nb_clients
		return f"Trajet(longueur : {long:.2f}km, contient {nb} clients)"
	
	
	def afficher(self, capacite :bool = False) :
		long = self.longueur
		nb = self.nb_clients
		capa = self.marchandise
		print(f"Trajet(longueur : {long:.2f}km, contient {nb} clients, {capa if capacite else [e.id for e in self.clients]})")



	def ajouter_client(self, indice :int, client :Client) :
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



	def retirer_client(self, indice :int) -> Client :
		"""
		Retire un client de l'itinéraire.

		Paramètres
		----------
		indice : int
			Indice du client dans la liste non vide 'clients'.

		Renvoie
		-------
		Le client se trouvant à l'indice passé en paramètre.
		"""
		assert isinstance(indice, int) and 0 <= indice < self.nb_clients and self.nb_clients > 0

		self.longueur += self.dist_retirer_client(indice)
		cli = self.clients.pop(indice)
		self.nb_clients -= 1
		self.marchandise -= cli.demande
		return cli



	def dist_ajouter_client(self, indice :int, client :Client) -> float :
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
		La différence positive de distance entre avant et après l'ajout du client.
		"""
		assert isinstance(client, Client)
		assert isinstance(indice, int) and indice >= 0

		if self.nb_clients == 0 :
			cli0 = self.depot
			cli1 = self.depot
		elif indice == 0 :
			cli0 = self.depot
			cli1 = self.clients[0]
		elif indice >= self.nb_clients :
			cli0 = self.clients[-1]
			cli1 = self.depot
		else :
			cli0 = self.clients[indice-1]
			cli1 = self.clients[indice]

		return distance(cli0, client) + distance(cli1, client) - distance(cli0, cli1)



	def dist_retirer_client(self, indice :int) -> float :
		"""
		Calcule et renvoie la différence de distance entre avant et après le retrait du client.

		Paramètres
		----------
		indice : int
			Indice du client dans la liste non vide 'clients'.

		Renvoie
		-------
		La différence négative de distance entre avant et après le retrait du client.
		"""
		assert isinstance(indice, int) and 0 <= indice < self.nb_clients and self.nb_clients > 0

		client = self.clients[indice]
		if self.nb_clients == 1 :
			cli0 = self.depot
			cli1 = self.depot
		elif indice == 0 :
			cli0 = self.depot
			cli1 = self.clients[1]
		elif indice == self.nb_clients - 1 :
			cli0 = self.clients[-2]
			cli1 = self.depot
		else :
			cli0 = self.clients[indice-1]
			cli1 = self.clients[indice+1]

		return distance(cli0, cli1) - distance(cli0, client) - distance(client, cli1)



	def dist_remplacer_client(self, indice :int, nouveau :Client) -> float :
		"""
		Calcule et renvoie la différence de distance entre avant et après le remplacement du client.

		Paramètres
		----------
		indice : int
			Indice du client à remplacer dans la liste non vide 'clients'.
		nouveau : Client
			Client utilisé pour le remplacement.

		Renvoie
		-------
		La différence de distance entre avant et après le remplacement du client.
		"""
		assert isinstance(nouveau, Client) and self.nb_clients > 0
		assert isinstance(indice, int) and 0 <= indice < self.nb_clients

		vieux = self.clients[indice]
		if self.nb_clients == 1 :
			cli0 = self.depot
			cli1 = self.depot
		elif indice == 0 :
			cli0 = self.depot
			cli1 = self.clients[1]
		elif indice == self.nb_clients-1 :
			cli0 = self.clients[-2]
			cli1 = self.depot
		else :
			cli0 = self.clients[indice-1]
			cli1 = self.clients[indice+1]

		return distance(cli0, nouveau) + distance(nouveau, cli1) - distance(cli0, vieux) - distance(vieux, cli1)





class Flotte :

	__slots__ = "capacite", "longueur", "nb_trajets", "trajets"

	def __init__(self, capacite :int = 0) :
		self.capacite = capacite
		self.longueur = 0.0
		self.nb_trajets = 0
		self.trajets = []


	def __repr__(self) -> str :
		long = self.longueur
		nb = self.nb_trajets
		return f"Flotte(longueur : {long:.2f}km, contient {nb} camions)"


	def afficher(self, capacite :bool = False) :
		print(self)
		for t in self.trajets:
			t.afficher(capacite)
		print()



	def ajouter_trajet(self, trajet :Trajet) :
		"""
		Ajoute un itinéraire de livraison.

		Paramètres
		----------
		trajet : Trajet
			Itinéraire de livraison à ajouter.
		"""
		assert isinstance(trajet, Trajet) and trajet.marchandise <= self.capacite

		self.trajets.append(trajet)
		self.longueur += trajet.longueur
		self.nb_trajets += 1



	def retirer_trajet(self, indice :int) -> Trajet :
		"""
		Retire et renvoie un itinéraire de livraison.

		Paramètres
		----------
		indice : int
			Indice de l'itinéraire dans la liste 'trajets'.

		Renvoie
		-------
		L'itinéraire de livraison qui a été retiré.
		"""
		assert isinstance(indice, int) and 0 <= indice < self.nb_trajets

		t = self.trajets.pop(indice)
		self.longueur -= t.longueur
		self.nb_trajets -= 1
		return t
