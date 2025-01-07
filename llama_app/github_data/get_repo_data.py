from config.config import HEADERS
import requests
import base64

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


def get_file_decoded(owner, repo, file_name):
    """
    Pobiera plik z repozytorium i go dekoduje.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_name}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        file_content = response.json()["content"]
        decoded_content = base64.b64decode(file_content).decode("utf-8")
        return decoded_content.splitlines()
    else:
        print(f"Błąd pobierania pliku {file_name}: {response.status_code}")
        return []


def fetch_all_commits(repo_owner, repo_name, auth_token, branch="main"):
    """
    Pobiera wszystkie commity z danego repozytorium GitHub.
    :param repo_owner: Właściciel repozytorium (np. "octocat")
    :param repo_name: Nazwa repozytorium (np. "Hello-World")
    :param auth_token: Token dostępu do GitHub API (personal access token)
    :param branch: Nazwa gałęzi, dla której pobieramy commity (domyślnie "main")
    :return: Lista commitów zawierająca szczegółowe dane
    """
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    commits = []
    page = 1

    while True:
        # Pobierz commity dla danej strony
        params = {"sha": branch, "per_page": 100, "page": page}
        response = requests.get(base_url, headers=headers, params=params)

        if response.status_code != 200:
            raise Exception(f"Błąd pobierania commitów: {response.status_code}, {response.text}")

        data = response.json()

        # Jeśli nie ma więcej commitów, przerywamy pętlę
        if not data:
            break

        # Dodaj commity do listy
        commits.extend(data)
        page += 1

    return commits


def fetch_commit_details(repo_owner, repo_name, commit_sha, auth_token):
    """
    Pobiera szczegółowe dane o konkretnym commicie w repozytorium GitHub.
    :param repo_owner: Właściciel repozytorium (np. "octocat")
    :param repo_name: Nazwa repozytorium (np. "Hello-World")
    :param commit_sha: SHA konkretnego commita
    :param auth_token: Token dostępu do GitHub API (personal access token)
    :return: Słownik z detalami commita
    """
    base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits/{commit_sha}"
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/vnd.github.v3+json"
    }

    response = requests.get(base_url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Zwraca szczegółowe dane jako JSON
    else:
        raise Exception(f"Błąd pobierania szczegółów commita: {response.status_code}, {response.text}")
