import json
from bs4 import BeautifulSoup

def load_settings():
    """
    Loads bot settings from a JSON file.
    """
    with open('settings.json', 'r') as f:
        settings = json.load(f)
    return settings

def extract_usernames_from_html(html_content):
    """
    Extracts Instagram usernames from the provided HTML content.
    """
    # Verifica che il contenuto sia una stringa
    if not isinstance(html_content, str):
        raise ValueError("The HTML content must be a string.")

    # Utilizza BeautifulSoup per analizzare il contenuto HTML
    soup = BeautifulSoup(html_content, 'lxml')
    usernames = []

    # Trova tutti i link che contengono i nomi utente
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if "instagram.com" in href:
            # Estrai il nome utente dal link
            username = href.split("/")[-1]
            if username:
                usernames.append(username)

    return usernames
