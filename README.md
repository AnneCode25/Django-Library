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

## Auteur
Anne Villette
