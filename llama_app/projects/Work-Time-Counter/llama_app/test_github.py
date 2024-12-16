from config.config import GITHUB_TOKEN
import base64
import os
import requests

# Token osobisty GitHub (zastąp "your_token_here" swoim tokenem z GitHub)
GITHUB_TOKEN = GITHUB_TOKEN
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# Dane repozytorium
OWNER = "IgorUchnast"  # np. "octocat"
REPO = "Work-Time-Counter"  # np. "hello-world"

def get_repo_tree(owner, repo):
    """
    Pobiera pełną strukturę drzewa repozytorium.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()["tree"]
    else:
        print(f"Błąd: {response.status_code} - {response.json()}")
        return []

def get_file(owner, repo, file_name):
    """
    Pobiera plik .gitignore z repozytorium.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_name}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        return decoded_content.splitlines()
    else:
        print(f"Błąd pobierania pliku .gitignore: {response.status_code}")
        return []

def download_file(owner, repo, path, save_path):
    """
    Pobiera zawartość pliku i zapisuje go lokalnie.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode("utf-8")

        # Zapisywanie pliku lokalnie
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, "w", encoding="utf-8") as file:
            file.write(decoded_content)
        print(f"Pobrano: {save_path}")
    else:
        print(f"Błąd pobierania pliku {path}: {response.status_code}")


def download_python_files(owner, repo):
    tree = get_repo_tree(owner=owner, repo=repo)
    for item in tree:
        # Sprawdzamy tylko pliki .py
        if item["type"] == "blob" and item["path"].endswith(".py"):
            prefix = ".venv"
            # Work-Time-Counter/flask_app/.venv/
            if prefix in item['path']:
                continue
            else:
                file_path = item["path"]
                # print(file_path)
                save_path = os.path.join(repo, file_path)
                download_file(owner=owner, repo=repo, path= file_path, save_path=f"projects/{save_path}")

if __name__ == "__main__":
    # Pobierz wszystkie pliki .py z repozytorium, pomijając te w .gitignore
    download_python_files(OWNER, REPO)
