"""Configuration : chemins du projet + lecture des variables d'environnement.

Règle d'or : tout ce qui est personnel ou secret (lien DossierFacile, téléphone,
clés d'API plus tard) vit dans le fichier .env, qui n'est JAMAIS commité.
Le code, lui, ne contient que des noms de variables.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "annonces.json"
SITE_DIR = ROOT / "site"
TEMPLATE_FILE = ROOT / "templates" / "message.txt"

# Charge le fichier .env (s'il existe) dans les variables d'environnement.
load_dotenv(ROOT / ".env")


def get(name: str, default: str = "", required: bool = False) -> str:
    value = os.getenv(name, default)
    if required and not value:
        raise SystemExit(
            f"La variable {name} est absente de ton fichier .env "
            f"(copie .env.example en .env et remplis-la)."
        )
    return value
