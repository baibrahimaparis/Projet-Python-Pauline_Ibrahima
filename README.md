# Projet-Python-Pauline_Ibrahima
First Xperience — Application de suivi de recherche d’emploi 
Présentation et objectifs du projet
First Xperience est un prototype d’application web pensé pour accompagner les personnes en recherche d’emploi, en particulier les jeunes diplômés. Elle permet aux demandeurs d'emploi d'organiser, suivre et optimiser leurs candidatures grâce à un tableau de bord intelligent, des statistiques personnalisées, un outil de préparation aux entretiens, et l'accès direct à des offres d'emploi en ligne.
Ce projet a été développé en Python à l'aide du framework Streamlit.
Fonctionnalités principales 
Création et gestion de compte : Inscription / connexion / déconnexion (authentification sécurisée grâce au hachage SHA-256 des mot de passe)

Tableau de bord : Visualisation de toutes vos candidatures

Ajout de candidatures : Formulaire complet (entreprise, poste, secteur, date, notes, statut)

Statistiques : Taux de réponse, délai moyen, secteurs qui répondent le plus

Préparation entretien : Checklists, notes par entreprise, questions types

Offres d’emploi via API externe : Recherche d’offres selon un poste (API RapidAPI)

Structure du Dépôt
first_xperience/
├── Accueil.py            <-- Point d'entrée
├── pages/
│   ├── connexion.py
│   ├── creation_compte.py
│   ├── Mon_suivi.py
│   └── Offres_emploi.py           
├── donnees/              
│   ├── candidatures.csv
│   ├── notes_entretien.csv
│   ├── utilisateurs.csv
├── image_accueil.png
└── requirements.txt

Lancement et exécution
pip install -r requirements.txt
Puis lancez l'application via le point d'entrée :
streamlit run Accueil.py

Construit avec
Streamlit : Interface front et routing
Pandas : Gestion des données
Python / CSV : Stockage local des comptes, candidatures et notes entretien
RapidAPI (jSearch) : Recherche d’offres d’emploi
Pathlib : Gestion de fichier

Auteurs
GRILLON Pauline
BA Ibrahima
