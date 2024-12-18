from config.config import HEADERS, GITHUB_TOKEN
from github_data.get_repo_data import get_repo_tree, fetch_all_commits, fetch_commit_details
import requests
import base64
import os


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
        if item["type"] == "blob" and item["path"].endswith(".py"):
            prefix = ".venv"
            # Work-Time-Counter/flask_app/.venv/
            if prefix in item['path']:
                continue
            else:
                file_path = item["path"]
                save_path = os.path.join(repo, file_path)
                # print(save_path)
                download_file(owner=owner, repo=repo, path= file_path, save_path=f"projects/{save_path}")

def get_fisrt_commit_id(owner, repo, token):
    all_commits = fetch_all_commits(owner, repo, token)
    return all_commits[0]['sha']

def get_new_changes(owner, repo, token):
    # Pobierz ID pierwszego commita
    commit_id = get_fisrt_commit_id(owner=owner, repo=repo, token=token)
    
    # Pobierz szczegóły tego commita
    commit_details = fetch_commit_details(repo_owner=owner, repo_name=repo, commit_sha=commit_id, auth_token=token)
    
    # Zainicjuj strukturę dla szczegółów commita
    commit_changes = {
        'commit_id': commit_details['sha'],
        'author_name': commit_details['commit']['author']['name'],
        'date': commit_details['commit']['author']['date'],
        'message': commit_details['commit']['message'],
        'files_changed': []  # Pusta lista na zmiany w plikach
    }

    # Iteruj po plikach, w których były zmiany
    for file in commit_details['files']:
        commit_changes['files_changed'].append({
            'filename': file['filename'],
            'changes': file['changes'],
            'additions': file['additions'],
            'deletions': file['deletions']
        })

    # Zwróć szczegóły commita
    return commit_changes


def find_changed_files_paths(owner, repo, token): 
    commit_changes =  get_new_changes(owner=owner, repo=repo, token=token)
    changed_files = []
    for file_name in commit_changes['files_changed']:
        changed_files.append(file_name['filename'])
    return changed_files


def opne_file(file_path):
     with open(file_path, 'r', encoding='utf-8') as files:
        content = files.read()  # Wczytanie całej zawartości pliku
        return content

def get_new_changed_files(owner, repo, token):
    download_python_files(owner, repo)
    new_changed_files = get_changed_files(owner, repo, token)
    return new_changed_files

def get_changed_files(owner, repo, token):
    changed_files = find_changed_files_paths(owner, repo, token)
    tree = get_repo_tree(owner=owner, repo=repo)
    contents = []
    for file_path in changed_files:
        # print(file_path)
        for item in tree:
            if item["type"] == "blob" and item["path"].endswith(".py"):
                if file_path in item['path']:
                    project_path = "/Users/igoruchnast/Documents/PW/PBL5/FLASK_SERVER/llama_app/projects" 
                    save_path = f"{project_path}" + "/" + f"{repo}" + "/" +f"{item['path']}"
                    # save_path = os.path.join(repo, file_path)
                    # print(save_path)
                    content = opne_file(file_path=save_path)
                    # print(content)
                    contents.append(content)                    
    return contents  # Wyświetlenie zawartości pliku
                
                
