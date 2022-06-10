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

Pour créer le fichier `config.py`, copier `config.py.template` et renommer le fichier de manière à retirer `.template`.

### Pour générer la liste

- `zotero_api_key` : API Key pour Zotero 
- `zotero_group_id` : ID du groupe Zotero
- `zotero_user_id` : (opt) ID de l'utilisateur Zotero  

### Pour poster sur Gitlab (opt)

- `gitlab_base_url` : url vers l'instance Gitlab utilisée  
- `gitlab_access_token`: Access Token pour Gitlab
- `gitlab_project_id` : ID du projet Gitlab où sera postée la liste de références
- `gitlab_issue_iid` : IID de l'issue dans laquelle la liste de références sera postée

## Exécution

1. Activer et installer les dépendances dans un environnement virtuel
2. Remplir les informations de `config.py`
3. Lancer `run.py` avec la commande `python run.py` (ajouter `--post` pour poster le résultat sur Gitlab)
