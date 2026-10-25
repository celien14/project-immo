"""Génère le message de contact personnalisé pour une annonce.

Le modèle (templates/message.txt) est public et commité.
Les valeurs personnelles ({nom}, {telephone}, {lien_dossier}) viennent du .env.
"""

from . import config
from .storage import Annonce


class _Defaut(dict):
    """Laisse un champ vide au lieu de planter si une info manque."""

    def __missing__(self, key):
        return ""


def generer(annonce: Annonce) -> str:
    modele = config.TEMPLATE_FILE.read_text(encoding="utf-8")
    valeurs = _Defaut(
        titre=annonce.titre or "votre logement",
        ville=annonce.ville,
        prix=annonce.prix or "",
        surface=f"{annonce.surface:g}" if annonce.surface else "",
        url=annonce.url,
        nom=config.get("CONTACT_NOM", required=True),
        telephone=config.get("CONTACT_TELEPHONE"),
        email=config.get("CONTACT_EMAIL"),
        lien_dossier=config.get("DOSSIER_FACILE_URL", required=True),
    )
    return modele.format_map(valeurs).strip()
