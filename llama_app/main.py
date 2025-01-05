from github_data.save_file import get_new_changes, find_changed_files_paths,get_new_changed_files, get_files_before_latest_commit, open_file
# from github_data.get_repo_data import fetch_commit_details, fetch_all_commits
from config.config import OWNER, REPO, GITHUB_TOKEN
from llama_server import connect_to_llama
# Usuń pojedynczy plik


# Przykład użycia
if __name__ == "__main__":
    
    try:

        # print("**********************")
        # print(get_files_before_latest_commit(OWNER, REPO, GITHUB_TOKEN))
        # print("****************************************************************************************")
        # # print(get_new_changed_files(OWNER, REPO, GITHUB_TOKEN))
        # # print(get_new_changes(OWNER, REPO, GITHUB_TOKEN))
        # print("**********************")
        # print(find_changed_files_paths(OWNER, REPO, GITHUB_TOKEN))
        # print("**********************")
        # ************************************************************************

        evaluation_criteria = open_file("/Users/igoruchnast/Documents/PW/PBL5/FLASK_SERVER/llama_app/evaluation_criteria.txt")
        # prompt = f"Based on those cryteria {evaluation_criteria} evaluate those files after and before new commit. {}"
        msg = input("Start/Exit : ")
        if msg == "Start":
            while msg != "Exit":
                msg = input("Analiza nowego commita T/F: ")
                if msg == 'F':
                    continue
                elif msg == 'T':
                    # prompt = input("Co mam wykonać ? ")
                    files_before_new_commit = get_files_before_latest_commit(OWNER, REPO, GITHUB_TOKEN)
                    files_new = get_new_changed_files(OWNER, REPO, GITHUB_TOKEN)
                    prompt = f"Based on those cryteria {evaluation_criteria} evaluate and categorize commits into difrent commit category after and before new commit.
                        Files before new commit {files_before_new_commit}. Changed files after new commit {files_new}"
                    for file in files_new:
                        output = connect_to_llama(prompt_message=prompt)
                else:
                    continue

    except Exception as e:
        print(f"Błąd: {e}")

print("DUPADUPADUPADUPADUPADUPADUPADUPADUPADUPADUPADUPADUPA")