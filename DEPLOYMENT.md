# Déploiement sur Render avec GitHub

## Étapes de déploiement

### 1. Prérequis
- Compte Render (https://render.com/)
- Compte GitHub avec le projet poussé
- Le projet est déjà configuré pour Render

### 2. Configuration du projet
Le projet contient déjà :
- `render.yaml` : Fichier de configuration Render
- `build.sh` : Script de build
- `requirements.txt` : Dépendances Python
- Configuration Django pour la production

### 3. Déploiement

#### Étape A : Pousser le code sur GitHub
```bash
git add .
git commit -m "Configuration pour déploiement Render"
git push origin main
```

#### Étape B : Créer un compte Render
1. Allez sur https://render.com/
2. Créez un compte avec GitHub
3. Autorisez Render à accéder à vos dépôts

#### Étape C : Créer le Web Service
1. Dans le dashboard Render, cliquez sur "New +"
2. Choisissez "Web Service"
3. Sélectionnez votre dépôt GitHub `bibliotheque`
4. Render détectera automatiquement le `render.yaml`
5. Confirmez la configuration

#### Étape D : Configurer la base de données
1. Créez une base de données PostgreSQL :
   - Cliquez sur "New +"
   - Choisissez "PostgreSQL"
   - Donnez un nom (ex: `bibliotheque-db`)
2. Une fois créée, allez dans les settings de la base de données
3. Copiez la "Connection URL"
4. Ajoutez cette URL comme variable d'environnement `DATABASE_URL` dans votre web service

#### Étape F : Variables d'environnement
Assurez-vous que ces variables sont configurées :
- `SECRET_KEY` : Généré automatiquement par Render
- `DEBUG` : `false`
- `DATABASE_URL` : URL de votre base PostgreSQL
- `PYTHON_VERSION` : `3.11.0`

### 4. Vérification du déploiement
- Render déploiera automatiquement votre application
- Vous pouvez suivre les logs dans le dashboard
- L'application sera accessible via l'URL fournie par Render

### 5. Commandes utiles en local
```bash
# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Lancer le serveur de développement
python manage.py runserver
```

## Fichiers modifiés pour le déploiement

### render.yaml
Configuration du service web Render avec :
- Python 3.11.0
- Build command personnalisée
- Gunicorn comme serveur
- Variables d'environnement sécurisées

### settings.py
Mises à jour pour la production :
- Configuration dynamique de la base de données
- Support des variables d'environnement
- Configuration des fichiers statiques avec WhiteNoise
- ALLOWED_HOSTS configuré pour Render

### build.sh
Script d'installation et de configuration :
- Installation des dépendances
- Collecte des fichiers statiques
- Migration de la base de données

## Support
En cas de problème :
1. Vérifiez les logs de déploiement sur Render
2. Assurez-vous que toutes les variables d'environnement sont configurées
3. Vérifiez que la base de données est accessible
4. Consultez la documentation Render : https://render.com/docs
