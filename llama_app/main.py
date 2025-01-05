from github_data.save_file import download_python_files, get_new_changes, find_changed_files_paths, get_changed_files,get_new_changed_files, open_file
from github_data.get_repo_data import fetch_commit_details, fetch_all_commits
from config.config import OWNER, REPO, GITHUB_TOKEN
from llama_server import connect_to_llama
# Usuń pojedynczy plik


# Przykład użycia
if __name__ == "__main__":
    
    try:
        # get_new_changed_files(OWNER,REPO,GITHUB_TOKEN)
        # prompt = "Powiedz mi co się dzieje w tym kodzie wytłumacz mi go?"
        # tab =  " msg = input('Start/Exit : '')"
        # output = connect_to_llama(prompt_message=prompt, prompt_data=tab)
        # print(output)
        # ************************************************************************
        # print("DUPA")
        # print(fetch_all_commits)

        # print(download_python_files(OWNER, REPO))
        print("**********************")
        print(get_new_changes(OWNER, REPO, GITHUB_TOKEN))
        print("**********************")
        print(find_changed_files_paths(OWNER, REPO, GITHUB_TOKEN))
        print("**********************")
        # print(get_changed_files(OWNER, REPO, GITHUB_TOKEN))
        # get_changed_files(OWNER, REPO, GITHUB_TOKEN)
        # print(get_new_changed_files(OWNER, REPO, GITHUB_TOKEN))
        # Pobierz wszystkie pliki .py z repozytorium, pomijając te w .gitignore
        # download_python_files(OWNER, REPO)

        # ************************************************************************

        # msg = input("Start/Exit : ")
        # if msg == "Start":
        #     while msg != "Exit":
        #         msg = input("Analiza nowego commita T/F: ")
        #         if msg == 'F':
        #             continue
        #         elif msg == 'T':
        #             prompt = input("Co mam wykonać ? ")
        #             files_new = get_new_changed_files(OWNER, REPO, GITHUB_TOKEN)
        #             for file in files_new:
        #                 output = connect_to_llama(prompt_message=prompt, prompt_data=file)
        #         else:
                    # continue

    except Exception as e:
        print(f"Błąd: {e}")

