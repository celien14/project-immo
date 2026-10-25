# Répertoire Immo

Petit outil perso pour suivre mes candidatures de location : je stocke les annonces
(Leboncoin, Jinka, SeLoger, PAP…), je génère un message de contact personnalisé avec
le lien de mon dossier, et je publie un tableau de bord sur Netlify.

Projet d'apprentissage : un SDLC miniature (code → git → GitHub → déploiement → sécurité).

## Installation

```bash
uv sync                 # installe les dépendances listées dans pyproject.toml
cp .env.example .env    # puis remplis .env avec tes vraies valeurs (sous Windows : copy)
```

## Utilisation

```bash
uv run main.py add "https://www.leboncoin.fr/..." --titre "Studio 25 m²" --prix 1050 --surface 25 --ville "Issy"
uv run main.py list
uv run main.py message 1 --ouvrir    # affiche le message et ouvre l'annonce
uv run main.py statut 1 contacte
uv run main.py build                 # régénère site/index.html
```

Statuts possibles : `a_contacter`, `contacte`, `visite`, `dossier_envoye`, `refuse`, `accepte`.

## Structure

```
main.py              point d'entrée
immo/cli.py          les commandes (add, list, message…)
immo/storage.py      lecture/écriture de data/annonces.json
immo/message.py      génération du message à partir du modèle
immo/site.py         génération du site statique
immo/config.py       chemins + lecture du .env
templates/message.txt  modèle de message (public)
.env                 mes infos perso et secrets (jamais commité)
site/                ce que Netlify publie
```

Feuille de route : voir [docs/ROADMAP.md](docs/ROADMAP.md).
