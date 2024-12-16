from github_data.save_file import download_python_files, get_new_changes, find_changed_files
from config.config import OWNER, REPO, GITHUB_TOKEN
import os

# Usuń pojedynczy plik


# Przykład użycia
if __name__ == "__main__":
    
    try:
        # file_path = "/Users/igoruchnast/Documents/PW/PBL5/FLASK_SERVER/llama_app/projects/Work-Time-Counter"
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        #     print(f"Plik '{file_path}' został usunięty.")
        # else:
        #     print(f"Plik '{file_path}' nie istnieje.")
        # delete_file("/Users/igoruchnast/Documents/PW/PBL5/FLASK_SERVER/llama_app/projects/Work-Time-Counter")
        # print(find_changed_files(OWNER, REPO, GITHUB_TOKEN))
        # print(get_new_changes(OWNER, REPO, GITHUB_TOKEN))
        # Pobierz wszystkie pliki .py z repozytorium, pomijając te w .gitignore
        download_python_files(OWNER, REPO)

    except Exception as e:
        print(f"Błąd: {e}")

