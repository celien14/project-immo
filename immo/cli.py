"""Interface en ligne de commande : c'est le "point d'entrée" de l'app.

Exemples (depuis le terminal de VS Code) :
  uv run main.py add "https://www.leboncoin.fr/..." --titre "Studio 25 m²" --prix 1050 --surface 25 --ville Issy
  uv run main.py list
  uv run main.py message 1 --ouvrir
  uv run main.py statut 1 contacte
  uv run main.py build
"""

import argparse
import webbrowser

from . import message, site, storage


def cmd_add(args):
    annonces = storage.charger()
    if any(a.url == args.url for a in annonces):
        raise SystemExit("Cette annonce est déjà dans ton répertoire.")
    a = storage.Annonce(
        id=storage.prochain_id(annonces),
        url=args.url,
        titre=args.titre,
        prix=args.prix,
        surface=args.surface,
        ville=args.ville,
        source=storage.detecter_source(args.url),
        notes=args.notes,
    )
    annonces.append(a)
    storage.sauvegarder(annonces)
    print(f"Annonce #{a.id} ajoutée ({a.source}).")


def cmd_list(args):
    annonces = storage.charger()
    if args.statut:
        annonces = [a for a in annonces if a.statut == args.statut]
    if not annonces:
        print("Aucune annonce.")
        return
    print(f"{'#':>3}  {'statut':<15} {'loyer':>7} {'m²':>5}  {'ville':<14} titre")
    for a in annonces:
        prix = f"{a.prix}€" if a.prix else "-"
        surf = f"{a.surface:g}" if a.surface else "-"
        print(f"{a.id:>3}  {a.statut:<15} {prix:>7} {surf:>5}  {a.ville[:14]:<14} {a.titre or a.url}")


def cmd_message(args):
    annonces = storage.charger()
    a = storage.trouver(annonces, args.id)
    print("-" * 60)
    print(message.generer(a))
    print("-" * 60)
    if args.ouvrir:
        webbrowser.open(a.url)
        print("Annonce ouverte dans le navigateur : colle le message dans le formulaire de contact.")


def cmd_statut(args):
    annonces = storage.charger()
    a = storage.trouver(annonces, args.id)
    a.statut = args.statut
    storage.sauvegarder(annonces)
    print(f"Annonce #{a.id} -> {a.statut}")


def cmd_supprimer(args):
    annonces = storage.charger()
    a = storage.trouver(annonces, args.id)
    annonces.remove(a)
    storage.sauvegarder(annonces)
    print(f"Annonce #{a.id} supprimée.")


def cmd_build(args):
    chemin = site.construire(storage.charger())
    print(f"Site généré : {chemin}")


def main(argv=None):
    p = argparse.ArgumentParser(prog="immo", description="Répertoire d'annonces immobilières")
    sub = p.add_subparsers(dest="commande", required=True)

    s = sub.add_parser("add", help="ajouter une annonce")
    s.add_argument("url")
    s.add_argument("--titre", default="")
    s.add_argument("--prix", type=int, help="loyer CC en €")
    s.add_argument("--surface", type=float, help="surface en m²")
    s.add_argument("--ville", default="")
    s.add_argument("--notes", default="")
    s.set_defaults(func=cmd_add)

    s = sub.add_parser("list", help="lister les annonces")
    s.add_argument("--statut", choices=storage.STATUTS)
    s.set_defaults(func=cmd_list)

    s = sub.add_parser("message", help="générer le message de contact")
    s.add_argument("id", type=int)
    s.add_argument("--ouvrir", action="store_true", help="ouvrir l'annonce dans le navigateur")
    s.set_defaults(func=cmd_message)

    s = sub.add_parser("statut", help="changer le statut d'une annonce")
    s.add_argument("id", type=int)
    s.add_argument("statut", choices=storage.STATUTS)
    s.set_defaults(func=cmd_statut)

    s = sub.add_parser("supprimer", help="supprimer une annonce")
    s.add_argument("id", type=int)
    s.set_defaults(func=cmd_supprimer)

    s = sub.add_parser("build", help="générer le site statique pour Netlify")
    s.set_defaults(func=cmd_build)

    args = p.parse_args(argv)
    args.func(args)
