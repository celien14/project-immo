"""Stockage des annonces dans un simple fichier JSON (data/annonces.json).

Pourquoi un JSON et pas une base de données ? Pour la v0, c'est lisible à l'oeil
dans VS Code et chaque modification apparaît clairement dans un `git diff`.
On pourra migrer vers SQLite ou une base hébergée plus tard.
"""

import json
from dataclasses import asdict, dataclass, field
from datetime import date
from urllib.parse import urlparse

from .config import DATA_FILE

STATUTS = ["a_contacter", "contacte", "visite", "dossier_envoye", "refuse", "accepte"]

SOURCES = {
    "leboncoin.fr": "leboncoin",
    "jinka.fr": "jinka",
    "seloger.com": "seloger",
    "pap.fr": "pap",
    "bienici.com": "bienici",
    "logic-immo.com": "logic-immo",
    "lacartedescolocs.fr": "lacartedescolocs",
}


@dataclass
class Annonce:
    id: int
    url: str
    titre: str = ""
    prix: int | None = None  # loyer mensuel charges comprises, en euros
    surface: float | None = None  # en m²
    ville: str = ""
    source: str = ""
    statut: str = "a_contacter"
    notes: str = ""
    ajoutee_le: str = field(default_factory=lambda: date.today().isoformat())

    @property
    def prix_m2(self) -> float | None:
        if self.prix and self.surface:
            return round(self.prix / self.surface, 1)
        return None


def detecter_source(url: str) -> str:
    domaine = urlparse(url).netloc.lower().removeprefix("www.")
    for cle, nom in SOURCES.items():
        if domaine.endswith(cle):
            return nom
    return domaine or "inconnue"


def charger() -> list[Annonce]:
    if not DATA_FILE.exists():
        return []
    raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return [Annonce(**item) for item in raw]


def sauvegarder(annonces: list[Annonce]) -> None:
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    contenu = json.dumps([asdict(a) for a in annonces], ensure_ascii=False, indent=2)
    DATA_FILE.write_text(contenu + "\n", encoding="utf-8")


def trouver(annonces: list[Annonce], annonce_id: int) -> Annonce:
    for a in annonces:
        if a.id == annonce_id:
            return a
    raise SystemExit(f"Aucune annonce avec l'id {annonce_id}. Tape `list` pour voir les ids.")


def prochain_id(annonces: list[Annonce]) -> int:
    return max((a.id for a in annonces), default=0) + 1
