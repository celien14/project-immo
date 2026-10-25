# Feuille de route (SDLC miniature)

## Phase 1 : les fondations (aujourd'hui)
- [ ] Code v0 : répertoire d'annonces en ligne de commande + message de contact
- [ ] Premier commit propre (avec `.gitignore` et `.env` exclu)
- [ ] Dépôt GitHub + `git push`
- [ ] Déploiement Netlify branché sur GitHub (chaque push = mise en ligne)

## Phase 2 : le workflow d'un dev
- [ ] Travailler sur une branche (`feature/...`), ouvrir une Pull Request, merger
- [ ] Ajouter des tests automatiques (`pytest`)
- [ ] CI avec GitHub Actions : les tests tournent à chaque push

## Phase 3 : l'automatisation (là où les secrets apparaissent)
- [ ] Envoi automatique d'emails aux agences via une API d'emailing (clé d'API = secret)
- [ ] Ingestion des alertes Jinka / Leboncoin reçues par email (Gmail API = OAuth client secret)
- [ ] Variables d'environnement côté Netlify / GitHub Actions (secrets de CI)

## Phase 4 : GitGuardian
- [ ] Commiter volontairement un faux secret et observer ce qui se passe (historique git, GitHub public)
- [ ] Brancher le dépôt sur la plateforme GitGuardian (détection, incidents, remédiation)
- [ ] Installer `ggshield` en hook pre-commit : bloquer le secret AVANT le commit
- [ ] `ggshield` dans GitHub Actions : bloquer le secret dans la CI
- [ ] Remédiation : révoquer, réécrire l'historique, comprendre pourquoi supprimer le fichier ne suffit pas

## Limites assumées
Leboncoin et la plupart des portails interdisent dans leurs CGU les robots qui
aspirent les annonces ou envoient des messages automatiquement (anti-bot, risque de
bannissement du compte). L'outil reste donc semi-automatique sur ces sites :
il prépare le message et ouvre l'annonce, l'envoi final se fait à la main.
L'automatisation complète vise les canaux qui la permettent (email direct aux agences).
