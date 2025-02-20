class Client :

	__slots__ = "id", "pos", "demande", "intervalle_livraison", "temps_livraison"

	def __init__(self, id: int, pos: tuple[int, int], intervalle_livraison: tuple[int, int], temps_livraison: int = 0, demande: int = 0):
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

	def __init__(self):
		self.longueur = 0
		self.nb_clients = 0
		self.clients = []






class Flotte :

	__slots__ = "capacite", "nb_camions", "camions", "trajets"

	def __init__(self, capacite: int):
		self.capacite = capacite
		self.nb_camions = 0
		self.camions = []
		self.trajets = []

	def ajouter_camion(self, marchandise: int, trajet: Trajet):
		if marchandise <= self.capacite:
			self.camions.append(marchandise)
			self.trajets.append(trajet)
			self.nb_camions += 1
		else:
			raise ValueError ("Quantité supérieure à la capacité maximale !")
