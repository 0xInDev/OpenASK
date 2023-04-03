# OpenASK

OpenASK est un projet open-source développé par les administrateurs d'InDev, ayant pour objectif de fournir une solution flexible et robuste pour la création et la gestion de sondages, d'évaluations, d'enquêtes et d'autres applications basées sur des questions-réponses.

## Caractéristiques

- Backend solide et performant
- Possibilité de créer des clients personnalisés pour différentes interfaces
- Adaptable à diverses utilisations, telles que les sondages, les évaluations ou les enquêtes
- Facilite la collaboration et la contribution des utilisateurs

## Contribuer

N'importe qui peut contribuer à ce projet en proposant des améliorations, en signalant des problèmes ou en développant des clients pour des interfaces personnalisées. Ensemble, nous pouvons créer une solution complète et polyvalente pour répondre à divers besoins en matière de questions-réponses.

## Licence

Ce projet est distribué sous une licence open-source. Pour plus d'informations, consultez le fichier `LICENSE` inclus dans ce dépôt.

## Contact

Pour toute question ou suggestion concernant OpenASK, n'hésitez pas à nous contacter. Nous sommes impatients de travailler avec vous pour améliorer et étendre les fonctionnalités de cette plateforme.

## Installation of requirements

```bash
python -m pip install -r requirements.txt

python manage.py makemigrations

python manage.py makemigrations api

python manage.py migrate
```

## for user creation

```bash
python manage.py createsuperuser

```
## Run server

```bash
python manage.py runserver
```
