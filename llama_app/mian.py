from github_data.save_file import download_python_files, get_new_changes, find_changed_files_paths, get_changed_files
from github_data.get_repo_data import fetch_commit_details
from config.config import OWNER, REPO, GITHUB_TOKEN
import os

# Usuń pojedynczy plik


# Przykład użycia
if __name__ == "__main__":
    
    try:
        # print(download_python_files(OWNER, REPO))
        print(find_changed_files_paths(OWNER, REPO, GITHUB_TOKEN))
        print("**********************")
        print(get_changed_files(OWNER, REPO, GITHUB_TOKEN))
        # print(get_new_changes(OWNER, REPO, GITHUB_TOKEN))
        # Pobierz wszystkie pliki .py z repozytorium, pomijając te w .gitignore
        # download_python_files(OWNER, REPO)

    except Exception as e:
        print(f"Błąd: {e}")

