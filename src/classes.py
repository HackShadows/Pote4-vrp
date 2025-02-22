class Client :

	__slots__ = "id", "pos", "demande", "intervalle_livraison", "temps_livraison"

	def __init__(self, id: int, pos: tuple[int, int], intervalle_livraison: tuple[int, int], temps_livraison: int = 0, demande: int = 0) -> None:
		self.id = id
		self.pos = pos
		self.demande = demande
		self.intervalle_livraison = intervalle_livraison
		self.temps_livraison = temps_livraison


	def __repr__(self) -> str :
		x, y = self.pos
		début, fin = self.intervalle_livraison
		temps = self.temps_livraison
		return f"Client(id: {self.id}, position: ({x} {y}), livraison entre {début} et {fin}, demande: {self.demande}, temps de livraison: {temps})"





class Trajet :

	__slots__ = "longueur", "nb_clients", "clients"

	def __init__(self) -> None:
		self.longueur = 0
		self.nb_clients = 0
		self.clients = []

	def __repr__(self) -> str :
		long = self.longueur
		nb = self.nb_clients
		return f"Trajet(longueur : {long}km, contient {nb} clients)"
	
	def ajouter_client(self, client: Client) -> None:
		"""
		Ajoute un client à la feuille de route.

		Paramètres
		----------
		client : Client
			Client à ajouter dans l'itinéraire de livraison.

		Raises
		------
		ValueError
			Mauvaise saisie de client.
		"""
		try:
			assert type(client) == Trajet
			self.clients.append(client)
			self.nb_clients += 1
		except AssertionError:
			raise ValueError ("Paramètre incorrect !")
	
	def retirer_client(self, indice: int) -> Client:
		"""
		Retire un client de l'itinéraire, et le renvoie.

		Paramètres
		----------
		indice : int
			Indice du client dans la liste clients.

		Retourne
		-------
		Le client se trouvant à l'indice passé en paramètre

		Raises
		------
		ValueError
			Mauvaise saisie de l'indice.
		"""
		try:
			assert type(indice) == int and indice < self.nb_clients and indice >= 0
			self.nb_clients -= 1
			return self.clients.pop(indice)
		except AssertionError:
			raise IndexError ("Indice invalide !")






class Flotte :

	__slots__ = "capacite", "longueur", "nb_camions", "camions", "trajets"

	def __init__(self, capacite: int) -> None:
		self.capacite = capacite
		self.longueur = 0
		self.nb_camions = 0
		self.camions = []
		self.trajets = []
	
	def __repr__(self) -> str :
		long = self.longueur
		nb = self.nb_camions
		return f"Flotte(longueur : {long}km, contient {nb} camions)"

	def ajouter_camion(self, marchandise: int, trajet: Trajet) -> None:
		"""
		Ajoute un camion et son itinéraire.

		Paramètres
		----------
		marchandise : int
			Quantité de marchandises contenue dans le camion.
		trajet : Trajet
			Itinéraire du camion

		Raises
		------
		ValueError
			Mauvaise saisie des paramètres.
		"""
		try:
			assert type(marchandise) == int and marchandise <= self.capacite
			assert type(trajet) == Trajet
			self.camions.append(marchandise)
			self.trajets.append(trajet)
			self.longueur += trajet.longueur
			self.nb_camions += 1
		except AssertionError:
			raise ValueError ("Paramètres incorrects !")
	
	def retirer_camion(self, indice: int) -> list[int, list[Client]]:
		"""
		Efface un camion et son itinéraire.

		Paramètres
		----------
		indice : int
			Indice du camion dans la liste camions

		Retourne
		-------
		Un tuple contenant respectivement la quantité de marchandises du camion, et la liste de ses clients

		Raises
		------
		ValueError
			Mauvaise saisie de l'indice.
		"""
		try:
			assert type(indice) == int and indice < self.nb_camions and indice >= 0
			c = self.camions.pop(indice)
			t = self.trajets.pop(indice)
			self.longueur -= t.longueur
			self.nb_camions -= 1
			return c, t.clients
		except AssertionError:
			raise IndexError ("Indice invalide !")
