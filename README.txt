FOOT ANALYTICS PRO — Version 2.0

CONTENU
- app.py : serveur FastAPI et endpoints de données
- static/index.html : interface responsive
- requirements.txt : dépendances Python
- render.yaml : configuration de déploiement Render

FONCTIONNALITÉS
- Interface compatible téléphone et ordinateur
- Calculateur Poisson : 1X2, BTTS, Over/Under 2,5 et top 3 scores
- Historique local des analyses
- Endpoints API pour matchs par date, recherche d'équipes, derniers matchs et statistiques d'équipe
- Intégration API-Football côté serveur (la clé n'est pas placée dans le navigateur)

POUR LANCER EN LOCAL
1. Installer Python 3.10+
2. Dans ce dossier : pip install -r requirements.txt
3. Définir la variable d'environnement APIFOOTBALL_KEY avec une clé API-Football valide.
4. Lancer : uvicorn app:app --reload
5. Ouvrir http://127.0.0.1:8000

POUR PUBLIER
1. Créer un dépôt GitHub privé ou public et y téléverser le contenu de ce dossier.
2. Sur Render, créer un nouveau Web Service à partir du dépôt.
3. Ajouter la variable d'environnement APIFOOTBALL_KEY dans les paramètres du service.
4. Déployer. Render fournira une adresse HTTPS publique.

IMPORTANT
- Je ne peux pas créer une URL publique active directement depuis ce chat sans accès à ton compte d'hébergement/dépôt. Le ZIP est prêt à déployer, mais le site n'est pas encore en ligne.
- API-Football demande une clé et impose des quotas et restrictions selon le plan. Vérifier le plan gratuit, les compétitions et limites avant utilisation.
- Le paramètre season est estimé à partir de l'année civile dans cet exemple et peut nécessiter adaptation selon les compétitions.
- Les moyennes pour le modèle de prédiction sont encore saisies manuellement dans l'interface; l'intégration complète des statistiques historiques dans les calculs sera une étape de développement suivante.
- Les prédictions sont des estimations et ne garantissent pas les résultats.
