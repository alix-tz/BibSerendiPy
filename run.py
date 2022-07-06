#!/usr/bin/env python

"""Execution file for Bib SerendiPy"""
__author__ = "Alix Chagué"
__copyright__ = "MIT"
__version__ = "0.1.1"

import argparse
import datetime
import os
import random

import requests

from dotenv import load_dotenv
from pyzotero import zotero
from dateutil import parser as dup


# Set Max number of suggestions
N_READ_MAX = 2
N_VAL_MAX = 4
N_CHECK_MAX = 2


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
    # load Zotero related variables
    zotero_api_key = os.environ.get("ZOTERO_API_KEY")
    zotero_group_id = os.environ.get("ZOTERO_GROUP_ID")
    zotero_user_id = os.environ.get("ZOTERO_USER_ID")

    # Load Zotero Collection
    zot = zotero.Zotero(library_id=zotero_group_id, library_type="group", api_key=zotero_api_key)
    items = zot.everything(zot.items())

    random.shuffle(items)

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
            if n_read < N_READ_MAX:
                n_read += 1
                if "high interest" in zot.item_tags(item["key"]):
                    bang = ":star: "
                else:
                    bang = ""
                refs_read.append(make_citation(item, bang))
        elif "à valider" in item_tags:
            if n_validate < N_VAL_MAX:
                n_validate += 1
                refs_validate.append(make_citation(item))
        elif not "vérifié" in item_tags:
            if not item['data'].get('itemType') in ["note", "attachment"]:
                if n_check_metadata < N_CHECK_MAX:
                    n_check_metadata += 1
                    refs_check_metadata.append(make_citation(item))
        if n_read == N_READ_MAX and n_validate == N_VAL_MAX and n_check_metadata == N_CHECK_MAX:
            break

    today = datetime.date.today()
    body += f"# {today.strftime('%d/%m/%Y')} (Semaine n°{today.isocalendar()[1]})\n"
    body += "\n## A lire:\n"
    body += "\n".join(refs_read)
    body += "\n\n## A valider:\n"
    body += "\n".join(refs_validate)
    body += "\n\n## Contrôler les métadonnées:\n"
    body += "\n".join(refs_check_metadata)
    return body


# Argument parsing ----------------------------------
arg_parser = argparse.ArgumentParser(description="Execution of Bib SerendiPy")
arg_parser.add_argument("--post", action="store_true", help="Trigger posting the list in a Gitlab issue as a comment")
args = arg_parser.parse_args()

load_dotenv()

print("Successfully loaded environment variables\n", 
        "Now building a list of reading suggestions",
        "based on Zotero Collection...", sep=" ")

# Build bibliographic list
body = body_builder()

print("List of reading suggestions successfully built.")

# Display or post to Gitlab
if args.post:
    # mpad Gitlab related variables from .env
    gitlab_base_url = os.environ.get("GITLAB_BASE_URL")
    gitlab_access_token = os.environ.get("GITLAB_ACCESS_TOKEN")
    gitlab_project_id = os.environ.get("GITLAB_PROJECT_ID")
    gitlab_issue_iid = os.environ.get("GITLAB_ISSUE_IID")
    if gitlab_base_url.endswith("/"):
        gitlab_base_url = gitlab_base_url[:-1]

    # Post Comment to Issue
    print("Preparing to post to Gitlab...")
    url = f"{gitlab_base_url}/api/v4/projects/{gitlab_project_id}/issues/{gitlab_issue_iid}/notes"
    r = requests.get(url, headers={"PRIVATE-TOKEN": gitlab_access_token})

    # Test connexion à Gitlab
    available = False
    if str(r.status_code) == "200":
        available = True

    if available:
        r = requests.post(url, headers={"PRIVATE-TOKEN": gitlab_access_token}, data={"body":body})
        print("Successfully posted to Gitlab!")
    else:
        print("Post failed: Gitlab was not available or the address is not correct.")
else:
    print("Here are the suggestions:\n")
    print(body)
