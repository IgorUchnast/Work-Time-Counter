from github_data.save_file import download_python_files, get_new_changes, find_changed_files_paths, get_changed_files,get_new_changed_files
from github_data.get_repo_data import fetch_commit_details
from config.config import OWNER, REPO, GITHUB_TOKEN
from llama_server import connect_to_llama
# Usuń pojedynczy plik


# Przykład użycia
if __name__ == "__main__":
    
    try:
        # print(download_python_files(OWNER, REPO))
        # print(find_changed_files_paths(OWNER, REPO, GITHUB_TOKEN))
        # print("**********************")
        # print(get_changed_files(OWNER, REPO, GITHUB_TOKEN))
        # print(get_new_changes(OWNER, REPO, GITHUB_TOKEN))
        # Pobierz wszystkie pliki .py z repozytorium, pomijając te w .gitignore
        # download_python_files(OWNER, REPO)
        msg = input("Start/Exit : ")
        if msg == "Start":
            while msg != "Exit":
                msg = input("Analiza nowego commita T/F: ")
                if msg == 'F':
                    continue
                elif msg == 'T':

                    files_old = get_changed_files(OWNER, REPO, GITHUB_TOKEN)
                    files_new = get_new_changed_files(OWNER, REPO, GITHUB_TOKEN)
                    tab = [files_old,files_new]
                    prompt = "Dostaniejsz do analizy pliki nowe (Najnowszy Commit) i stare (Poprzedni Commit) z projketu, który jest na githubie. Masz przeanalizować zmiany w plikach na podstawie zmiany w poszczególnych commitów. Powiedz mi jakie rónice w kodzie zostały znalezione, jakie kluczowe elementy zostały dodane"
                    output = connect_to_llama(prompt_message=prompt, prompt_data=tab)
                    print(output)
                else:
                    continue
    except Exception as e:
        print(f"Błąd: {e}")

