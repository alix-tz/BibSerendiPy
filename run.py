#!/usr/bin/env python

"""Execution file for Bib SerendiPy"""
__author__ = "Alix Chagué"
__copyright__ = "MIT"
__version__ = "0.1.1"

import argparse
import datetime

import requests

from pyzotero import zotero
from dateutil import parser as dup


# Functions ---------------------------------------
def get_authors(creators):
    authors = "(NA)"
    if creators:
        if len(creators) == 1:
            authors = creators[0].get('lastName', "(NA)")
        elif len(creators) == 2:
            authors = f"""{creators[0].get('lastName', "(NA)")} & {creators[1].get('lastName', "(NA)")}"""
        else:
            authors = f"""{creators[0].get('lastName', "(NA)")} et al."""
    return authors

def simple_date(date):
    new_date = "ND"
    if date:
        new_date = dup.parse(date).strftime("%Y")
    return new_date

def make_citation(item, bang=""):
    authors = get_authors(item['data'].get('creators'))
    date = simple_date(item['data'].get('date'))
    title = item['data'].get('title')
    ref_type = item['data'].get('itemType')
    doi = item["data"].get("DOI", "no doi")
    return f"- [ ] {bang}{authors}, {date}, *{title}* ({ref_type}). doi: {doi}"

def body_builder():
    # Import from config
    from config import zotero_api_key, zotero_group_id, zotero_user_id

    # Load Zotero Collection
    zot = zotero.Zotero(library_id=zotero_group_id, library_type="group", api_key=zotero_api_key)
    items = zot.everything(zot.items())

    # Explore Zotero Collection dans build reading list
    # Build Reading List
    body = ""

    refs_read = []
    refs_validate = []
    refs_check_metadata = []

    n_read = 0
    n_validate = 0
    n_check_metadata = 0

    for item in items:
        item_tags = zot.item_tags(item["key"])
        if "à lire" in item_tags:
            if n_read < 5:
                n_read += 1
                if "high interest" in zot.item_tags(item["key"]):
                    bang = ":star: "
                else:
                    bang = ""
                refs_read.append(make_citation(item, bang))
        elif "à valider" in item_tags:
            if n_validate < 5:
                n_validate += 1
                refs_validate.append(make_citation(item))
        elif not "vérifié" in item_tags:
            if n_check_metadata < 5:
                n_check_metadata += 1
                refs_check_metadata.append(make_citation(item))
        if n_read == 5 and n_validate == 5 and n_check_metadata == 5:
            break

    this_week = datetime.date.today().isocalendar() 
    body += f"# Cette semaine (n°{this_week[1]} de {this_week[0]}))\n\n"
    body += "## A lire:\n"
    body += "\n".join(refs_read)
    body += "\n## A valider:\n"
    body += "\n".join(refs_validate)
    body += "\n## Contrôler les métadonnées:\n"
    body += "\n".join(refs_check_metadata)
    return body


# Argument parsing ----------------------------------
arg_parser = argparse.ArgumentParser(description="Execution of Bib SerendiPy")
arg_parser.add_argument("--post", action="store_true", help="Trigger posting the list in a Gitlab issue as a comment")
args = arg_parser.parse_args()

body = body_builder()

# Display or post
if args.post:
    # trigger posting
    from config import gitlab_access_token, gitlab_project_id, gitlab_issue_iid, gitlab_base_url 

    if gitlab_base_url.endswith("/"):
        gitlab_base_url = gitlab_base_url[:-1]

    # Post Comment to Issue
    url = f"{gitlab_base_url}/api/v4/projects/{gitlab_project_id}/issues/{gitlab_issue_iid}/notes"
    r = requests.get(url, headers={"PRIVATE-TOKEN": gitlab_access_token})

    # Test connexion à Gitlab
    available = False
    if str(r.status_code) == "200":
        available = True

    if available:
        r = requests.post(url, headers={"PRIVATE-TOKEN": gitlab_access_token}, data={"body":body})
    else:
        print("Gitlab n'est pas disponible ou bien l'adresse n'est pas correcte.")

else:
    print(body)