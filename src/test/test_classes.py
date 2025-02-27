import unittest
from classes import *



class TestClassClient(unittest.TestCase) :

	def test_initialisation(self) :
		arguments = "id0", (4, 1000), (98, 123456), 10, 330
		client = Client(*arguments)
		self.assertEqual(client.id                  , arguments[0])
		self.assertEqual(client.pos                 , arguments[1])
		self.assertEqual(client.intervalle_livraison, arguments[2])
		self.assertEqual(client.temps_livraison     , arguments[3])
		self.assertEqual(client.demande             , arguments[4])
	
	def test_repr(self) :
		client = Client("id1", (4, 1000), (98, 123456), 10, 330)
		self.assertIsInstance(repr(client), str)





class TestClassTrajet(unittest.TestCase) :

	def test_initialisation(self) :
		depot = Client("id2", (4, 1000), (98, 123456))
		trajet = Trajet(client)
		self.assertEqual(trajet.longueur, 0.)
		self.assertEqual(trajet.nb_clients, 0)
		self.assertListEqual(trajet.clients, [])
		self.assertIs(trajet.depot, depot)

	def test_repr(self) :
		depot = Client("id3", (4, 1000), (98, 123456))
		trajet = Trajet(client)
		self.assertIsInstance(repr(trajet), str)
	
	def test_ajouter_client(self) :
		depot = Client("id4", (4, 1000), (98, 123456))
		trajet = Trajet(client)
		
