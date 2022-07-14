## Projet7: Implémentez un modèle de scoring

### Contexte du projet:
La société financière, intitulé "Prêt à dépenser", propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt.
L’entreprise souhaite mettre en œuvre un outil de “scoring crédit” pour calculer la probabilité qu’un client rembourse son crédit, puis classifie la demande en crédit accordé ou refusé. 
### Objectifs:
1. L’entreprise souhaite développer un algorithme de classification en s’appuyant sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.)
2. "Prêt à dépenser" décide de développer un dashboard interactif facilement exploitable par les chargés de relation client afin d’expliquer les décisions d’octroi de crédit, et de disposer des informations clients à explorer facilement.

### Le projet est structuré en 3 parties :
-	Notebook – le code de modélisation pour une classification binaire avec des classes déséquilibrées & le prétraitement de la prédiction ;
-	API - le code de déploiement des prédictions avec le meilleur modèle optimisé (utilisation FLASK);
-	Dashboard – le dashboard interactif contenant le code de restitution des données clients, récupération de prédiction et visualisation des caractéristiques importantes pour les clients (utilisation DASH)

## Le Dashboard interactif est déployé sur un serveur cloud et accessible online à l'adresse: http://162.19.76.116/
