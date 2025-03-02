"""
Met à disposition des fonctions permettant l'importation et l'exportation
des jeux de données dans le programme.
"""

from classes import Client

import re, warnings
from pathlib import Path

from typing import Any, IO





class ParsingError(Exception) :
	pass





MÉTADONNÉE_CONNUES = {
	"NAME"         : str,
	"COMMENT"      : str,
	"TYPE"         : str,
	"COORDINATES"  : str,
	"NB_DEPOTS"    : int,
	"NB_CLIENTS"   : int,
	"MAX_QUANTITY" : int,
}



_PATTERN_MÉTADONNÉES = re.compile(r"^([A-Z_]+)\s*:\s*(.*)\n$")
_PATTERN_ENTÊTE = re.compile(r"^([A-Z_]+)\s*\[(\s*(?:[a-zA-Z_][a-zA-Z0-9_]*\s*)+)\]\s*:\n$")





def _cherche_entête(nom_tableau :str, entête :list[str], données :list[str]) -> list[int] :
	"""
	Recherche les données dans 'entête' et lève une exception si elles n'existent pas.

	Paramètres
	----------
	nom_tablea : string
		Le nom du tableau auquel appartient l'entête. Demander pour donner plus d'information en cas d'erreur.
	entête : list of strings
		L'entête du tableau, l'ordre des attributs doit être conservé.
	données : list of strings
		Les données recherchées dans l'entête.
	
	Renvoie
	-------
	Une liste contenant pour chaque donnée, son index dans l'entête.

	Erreurs
	-------
	ParsingError
		La donnée n'a pas été trouvé dans l'entête.
	"""
	entête = {name.lower() : i for i, name in enumerate(entête)}

	résultat = list()
	for donnée in données :
		index = entête.get(donnée.lower())
		if index is None :
			raise ParsingError(f"Le tableau {nom_tableau} ne contient pas l'attribut '{donnée}'")
		résultat.append(index)
	
	return résultat



def importer_vrp(fichier :str|Path|IO[str]) -> tuple[dict[str, Any], list[Client], list[Client]] :
	"""
	Importe les données du fichier .vrp dans le programme.
	La fonction parse les métadonnées, puis se met à la recherche des tableaux 'DATA_DEPOTS' et 'DATA_CLIENTS'.

	Paramètres
	----------
	fichier : path_like
		Le nom du fichier à importer.
	fichier : stream_like
		Un flux ouvert sur le fichier à importer.
	
	Renvoie
	-------
	Un tuple contenant respectivement la liste des dépots et la liste des clients.

	Avertissements
	--------------
	UserWarning
		Un même tableau apparaît deux fois ou plus dans le fichier.

	Erreurs
	-------
	ParsingError
		Une métadonnée ou un entête est mal formé
	ParsingError
		Les tableaux recherchés ne sont pas trouvés.
	TypeError
		Une métadonnée ou une valeur d'un tableau n'a pas le bon type.
	ValueError
		La valeur d'une métadata n'est pas supportée.
	"""
	if isinstance(fichier, (str, Path)) :
		with open(fichier, 'r') as f :
			return importer_vrp(f)


	métadonnées = dict()
	for ligne in fichier :
		if ligne == "\n" : break

		match = _PATTERN_MÉTADONNÉES.match(ligne)
		if match is None or len(match.groups()) != 2 :
			raise ParsingError(f"La métadonné \"{ligne}\" ne suit pas le format \"<NOM_DE_LA_METADONNE> : <valeur>\".")
		nom, valeur = match.groups()

		typ = MÉTADONNÉE_CONNUES.get(nom)
		if typ is not None :
			try :
				valeur = typ(valeur)
			except Exception :
				raise TypeError(f"La métadonnée {{{nom!r} : {valeur!r}}} ne peut pas être converti en {typ.__name__}") from None

		métadonnées[nom] = valeur



	if (v := métadonnées.get("TYPE")) is not None and v != "vrptw" :
		raise ValueError(f"Type de données non supporté : \"{v}\" (attendu vrptw)")
	if (v := métadonnées.get("COORDINATES")) is not None and v != "cartesian" :
		raise ValueError(f"Type de coordonées non supporté : \"{v}\" (attendu cartesian)")



	contenu = dict()
	for ligne in fichier :

		match = _PATTERN_ENTÊTE.match(ligne)
		if match is None or len(match.groups()) != 2 :
			raise ParsingError(f"L'entête de tableau \"{ligne}\" ne suit pas le format \"<NOM_DU_TABLEAU> [ <nom_de_la_colonne> <...> ] :\"")
		nom, entête = match.groups()
		entête = entête.strip().split()

		if nom in contenu :
			warnings.warn(f"Le tableau {nom} est présent deux fois dans le fichier. Seul le second sera pris en compte.")

		tableau = list()
		for ligne in fichier :
			if ligne == "\n" : break
			tableau.append(ligne.strip().split())

		contenu[nom] = entête, tableau



	entête, tableau = contenu.get("DATA_DEPOTS", (None,None))
	if entête is None :
		raise ParsingError("Le fichier .vrp ne contient aucune information sur le(s) dépôt(s) (habituellement dans le tableau DATA_DEPOTS)")
	ID, X, Y, DÉBUT_H, FIN_H = _cherche_entête(
		"DATA_DEPOTS",
		entête,
		["idName", "x", "y", "readyTime", "dueTime"]
	)
	dépots  = [ Client(
		ligne[ID],
		(int(ligne[X]), int(ligne[Y])),
		(int(ligne[DÉBUT_H]), int(ligne[FIN_H]))
	) for ligne in tableau ]



	entête, tableau = contenu.get("DATA_CLIENTS", (None,None))
	if entête is None :
		raise ParsingError("Le fichier .vrp ne contient aucune information sur les clients (habituellement dans le tableau DATA_CLIENTS)")
	ID, X, Y, DÉBUT_H, FIN_H, QUANT, DURÉE = _cherche_entête(
		"DATA_CLIENTS",
		entête,
		["idName", "x", "y", "readyTime", "dueTime", "demand", "service"]
	)
	clients = [ Client(
		ligne[ID],
		(int(ligne[X]), int(ligne[Y])),
		(int(ligne[DÉBUT_H]), int(ligne[FIN_H])),
		int(ligne[QUANT]),
		int(ligne[DURÉE])
	) for ligne in tableau ]



	return métadonnées, dépots, clients
