import json
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def charger_json(nom_fichier):
    chemin = FIXTURES / nom_fichier

    with open(chemin, "r", encoding="utf-8") as fichier:
        return json.load(fichier)


def charger_referentiel():
    return charger_json("referentiel.json")


def charger_parties():
    return charger_json("parties.json")


def charger_indicateurs():
    return charger_json("indicateurs.json")
