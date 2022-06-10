# Bib SerendiPy

Un petit programme pour générer des listes courtes d'entrée bibliographiques, à lire, controler ou contempler.

## Pré-requis

Le programme utilise PyZotero pour interroger un collection bibliographique Zotero. Ensuite, les items sont sélectionné en fonction des *tags* qui leur sont associés.

Pour le moment, le programme cibles les tags suivants :

- "à lire" (pour les items qu'il faut lire...) 
- "à valider" (pour les items dont il faut confirmer qu'on les garde dans la collection)
- "vérifié" (pour les items dont on a controlé et corrigé les métadonnées)

## Dépendances

Le programme utilise des libraries Python externes :  

- `PyZotero`
- `Python-Dateutil`
- `Python-Dotenv`
- `Requests`

Pour executer le programme, il faut donc s'assurer d'installer ces dépendances (avec PiPy par exemple) à l'aide du fichier `requirements.txt`, de préférence dans un environnement virtuel.  

## Execution

Plusieurs informations externes sont requises et doivent être indiquées dans le fichier `config.py`. Attention, ces informations ne doivent pas être rendues publiques.  

Pour créer le fichier `.env`, copier `.env.template` et renommer le fichier de manière à retirer `.template`.

### Pour générer la liste

- `ZOTERO_API_KEY` : API Key pour Zotero 
- `ZOTERO_GROUP_ID` : ID du groupe Zotero
- `ZOTERO_USER_ID` : (opt) ID de l'utilisateur Zotero  

### Pour poster sur Gitlab (opt)

- `GITLAB_BASE_URL` : url vers l'instance Gitlab utilisée  
- `GITLAB_ACCESS_TOKEN`: Access Token pour Gitlab
- `GITLAB_PROJECT_ID` : ID du projet Gitlab où sera postée la liste de références
- `GITLAB_ISSUE_IID` : IID de l'issue dans laquelle la liste de références sera postée

## Exécution

1. Activer et installer les dépendances dans un environnement virtuel
2. Remplir les informations de `.env`
3. Lancer `run.py` avec la commande `python run.py` (ajouter `--post` pour poster le résultat sur Gitlab)
