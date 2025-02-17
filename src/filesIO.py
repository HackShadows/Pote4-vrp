from classes import Client

import re
from pathlib import Path

from typing import IO





METADONNEE_CONNUES = {
	"NAME"        : str,
	"COMMENT"     : str,
	"TYPE"        : str,
	"COORDINATES" : str,
	"NB_DEPOTS"   : int,
	"NB_CLIENTS"  : int,
	"MAX_QUANTIT" : int,
}





def importer_vrp(fichier :str|Path|IO[str]) -> tuple[list[Client], list[Client]] :
	if isinstance(fichier, (str, Path)) :
		with open(fichier, 'r') as f :
			return importer_vrp(f)
		

	métadonnés = dict()
	for ligne in fichier :
		if ligne == "\n" : break
		
		match = re.match(r"^([A-Z_]+)\w*:\w*(.*)\w*\n$", ligne)
		if match is None or len(match.groups()) != 2 :
			raise ValueError(f"La métadonné \"{ligne}\" ne suit pas le format \"[NOM_DE_LA_METADONNE] : [valeur]\".")
		nom, valeur = match.groups()
		
		typ = METADONNEE_CONNUES.get(nom)
		if typ is not None :
			try :
				valeur = typ(valeur)
			except Exception :
				raise TypeError(f"La métadonnée {{{nom} : {valeur}}} ne peut pas être converti en {typ.__name__}") from None
		
		métadonnés[nom] = valeur
	

	if (v := métadonnés.get("TYPE")) is not None and v != "vrptw" :
		raise ValueError(f"Type de données non supporté : \"{v}\" (attendu vrptw)")
	if (v := métadonnés.get("COORDINATES")) is not None and v != "cartesian" :
		raise ValueError(f"Type de coordonées non supporté : \"{v}\" (attendu cartesian)")
	


	dépots  = list()
	clients = list()

	ligne = next(fichier, None)
	match = re.match(r"([A-Z_]+)\w*\[([a-zA-Z_]+(\w+[a-zA-Z_]+)*)\]")



	dépots = list()
	for ligne in fichier :
		if ligne == "\n" : break

		...