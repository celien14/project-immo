"""Construit le tableau de bord statique (site/index.html) publié sur Netlify.

Attention : tout ce qui est écrit ici devient PUBLIC sur internet.
On n'y met donc jamais le lien du dossier, le téléphone ou le contenu du .env.
"""

from collections import Counter
from datetime import datetime
from html import escape

from .config import SITE_DIR
from .storage import STATUTS, Annonce

LIBELLES = {
    "a_contacter": "À contacter",
    "contacte": "Contacté",
    "visite": "Visite prévue",
    "dossier_envoye": "Dossier envoyé",
    "refuse": "Refusé",
    "accepte": "Accepté",
}


def _ligne(a: Annonce) -> str:
    prix = f"{a.prix} €" if a.prix else "–"
    surface = f"{a.surface:g} m²" if a.surface else "–"
    prix_m2 = f"{a.prix_m2} €/m²" if a.prix_m2 else "–"
    return f"""
      <tr>
        <td class="num">{a.id}</td>
        <td><a href="{escape(a.url)}" target="_blank" rel="noopener">{escape(a.titre or a.url)}</a>
            <div class="meta">{escape(a.source)} · ajoutée le {escape(a.ajoutee_le)}</div></td>
        <td>{escape(a.ville) or "–"}</td>
        <td class="num">{prix}</td>
        <td class="num">{surface}</td>
        <td class="num">{prix_m2}</td>
        <td><span class="badge {a.statut}">{LIBELLES.get(a.statut, a.statut)}</span></td>
      </tr>"""


def construire(annonces: list[Annonce]) -> str:
    compte = Counter(a.statut for a in annonces)
    stats = "".join(
        f'<div class="stat"><span class="n">{compte.get(s, 0)}</span>{LIBELLES[s]}</div>'
        for s in STATUTS
    )
    lignes = "".join(_ligne(a) for a in sorted(annonces, key=lambda a: a.id, reverse=True))
    vide = '<p class="vide">Aucune annonce pour l\'instant. Ajoute la première avec <code>uv run main.py add …</code></p>'
    maj = datetime.now().strftime("%d/%m/%Y à %H:%M")

    html = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Répertoire Immo</title>
<style>
  :root {{ --bg:#f7f6f3; --card:#fff; --ink:#1d1d1f; --mute:#6b6b70; --line:#e6e4df; --accent:#0b6e4f; }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg:#141416; --card:#1d1d20; --ink:#ececee; --mute:#9a9aa1; --line:#2c2c31; --accent:#3ccf91; }}
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; background:var(--bg); color:var(--ink); font:15px/1.5 system-ui, -apple-system, "Segoe UI", sans-serif; }}
  main {{ max-width:1100px; margin:0 auto; padding:32px 16px; }}
  h1 {{ margin:0 0 4px; font-size:28px; }}
  .sub {{ color:var(--mute); margin:0 0 24px; }}
  .stats {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:10px; margin-bottom:24px; }}
  .stat {{ background:var(--card); border:1px solid var(--line); border-radius:10px; padding:12px 14px; color:var(--mute); font-size:13px; }}
  .stat .n {{ display:block; font-size:24px; font-weight:650; color:var(--ink); }}
  .wrap {{ overflow-x:auto; background:var(--card); border:1px solid var(--line); border-radius:12px; }}
  table {{ width:100%; border-collapse:collapse; min-width:720px; }}
  th, td {{ text-align:left; padding:12px 14px; border-bottom:1px solid var(--line); vertical-align:top; }}
  th {{ font-size:12px; text-transform:uppercase; letter-spacing:.04em; color:var(--mute); }}
  tr:last-child td {{ border-bottom:0; }}
  .num {{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }}
  a {{ color:var(--accent); text-decoration:none; font-weight:550; }}
  .meta {{ color:var(--mute); font-size:12px; }}
  .badge {{ font-size:12px; padding:3px 8px; border-radius:99px; border:1px solid var(--line); white-space:nowrap; }}
  .badge.contacte, .badge.dossier_envoye {{ border-color:#3b82f6; color:#3b82f6; }}
  .badge.visite {{ border-color:#d97706; color:#d97706; }}
  .badge.accepte {{ border-color:var(--accent); color:var(--accent); }}
  .badge.refuse {{ color:var(--mute); text-decoration:line-through; }}
  .vide {{ padding:24px; color:var(--mute); }}
</style>
</head>
<body>
<main>
  <h1>Répertoire Immo</h1>
  <p class="sub">{len(annonces)} annonce(s) suivie(s) · mis à jour le {maj}</p>
  <section class="stats">{stats}</section>
  <div class="wrap">
    {"<table><thead><tr><th class='num'>#</th><th>Annonce</th><th>Ville</th><th class='num'>Loyer</th><th class='num'>Surface</th><th class='num'>Prix/m²</th><th>Statut</th></tr></thead><tbody>" + lignes + "</tbody></table>" if annonces else vide}
  </div>
</main>
</body>
</html>
"""
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    chemin = SITE_DIR / "index.html"
    chemin.write_text(html, encoding="utf-8")
    return str(chemin)
