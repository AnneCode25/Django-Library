# Logiciel de Gestion de Médiathèque

Un système de gestion pour la médiathèque "Notre livre, notre média" permettant de gérer les emprunts, les retours et le catalogue de médias.

## Fonctionnalités

### Application Bibliothécaire
- Gestion des membres (ajout, modification, suppression)
- Gestion des médias (livres, DVDs, CDs, jeux de plateau)
- Gestion des emprunts et retours
- Tableau de bord avec statistiques
- Système de logs pour suivre les activités

### Application Membre
- Consultation du catalogue des médias disponibles

## Installation

1. Cloner le repository
```bash
git clone [URL_DU_REPO]
```
2. Créer un environnement virtuel
```bash
python -m venv env
```
3. Activer l'environnement virtuel
```bash
# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```
4. Installer les dépendances
```bash
pip install -r requirements.txt
```
5. Effectuer les migrations
```bash
python manage.py migrate
```
6. Créer un superutilisateur
```bash
python manage.py createsuperuser
```
7. Lancer le serveur
```bash
python manage.py runserver
```

## Structure du projet
Le projet est organisé comme suit :

- home/ : Application page d'accueil
- librarian/ : Application des bibliothécaires
- member/ : Application des membres
- shared_models/ : Modèles partagés
- templates/ : Templates HTML
- logs/ : Fichiers de logs

## Règles métiers
- Un membre ne peut pas avoir plus de 3 emprunts simultanés 
- La durée d'emprunt est d'une semaine
- Un membre ayant un retard ne peut pas emprunter
- Les jeux de plateau sont uniquement consultables sur place

## Tests
Pour lancer les tests 
```bash
python manage.py test
```

## Logs
Les logs sont stockés dans le dossier logs/ et incluent :

- Les créations/modifications de membres
- Les emprunts et retours
- Les modifications du catalogue

## Technologies utilisées
- Django 5.1.2
- Python 3.12.6
- SQLite 3.45.3

Dépendances :
- asgiref 3.8.1
- sqlparse 0.5.1
- tzdata==2024.2

## Base de données de test

Une base de données de test est disponible avec des données exemple comprenant :
- Des membres
- Des médias (livres, DVDs, CDs, jeux de plateau)
- Des emprunts en cours et retournés

Pour installer ces données :

1. Créer et activer l'environnement virtuel :
```bash
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Linux/Mac
```
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```
3. Effectuer les migrations :
```bash
python manage.py migrate
```
4. Charger les données de test :
```bash
python manage.py loaddata fixtures/all_data.json
```

## Page d'erreur
1. Test des pages d'erreur en local
Pour tester les pages d'erreur personnalisées en développement :

- Définissez temporairement DEBUG = False dans settings.py
- Ajoutez 'localhost' et '127.0.0.1' à ALLOWED_HOSTS
- Lancez le serveur avec : python manage.py runserver --insecure
- Visitez une URL inexistante pour voir la page 404 personnalisée

⚠️ N'oubliez pas de remettre DEBUG = True après les tests en développement !
Pages d'erreur personnalisées

2. Le projet inclut des pages d'erreur personnalisées :

- 404 (Page non trouvée)


## Auteur
Anne Villette
