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
        print(get_new_changes(OWNER, REPO, GITHUB_TOKEN))
        # print("**********************")
        print(find_changed_files_paths(OWNER, REPO, GITHUB_TOKEN))
        # print("**********************")
        # ************************************************************************

        # evaluation_criteria = open_file("/Users/igoruchnast/Documents/PW/PBL5/FLASK_SERVER/llama_app/evaluation_criteria.txt")
        evaluation_criteria = """ Commit Categories, Scales, and Evaluation Criteria
1. Bug FixesDescription: Commits in this category address existing bugs in the code.Evaluation Criteria:
* Does the fix fully resolve the issue? (1-5)
* Are the changes minimal and precise? (1-5)
* Does the fix avoid introducing new potential bugs? (1-5)Scale: 1-5 (where 5 represents the highest quality fix).
2. Feature AdditionsDescription: Commits introducing new features or components.Evaluation Criteria:
* How well is the feature implemented? (1-10)
* Is the code modular and easy to extend? (1-5)
* Are adequate tests provided for the new feature? (1-5)Scale: 1-10 (where 10 represents a fully thought-out and comprehensive implementation).
3. Code RefactoringDescription: Commits that restructure code without adding new features.Evaluation Criteria:
* Does the refactoring improve code readability? (1-5)
* Does it enhance performance or scalability? (1-5)
* Does it preserve existing functionality? (1-5)Scale: 1-5 (where 5 represents flawless execution).
4. Documentation UpdatesDescription: Commits related to documentation, e.g., README files or code comments.Evaluation Criteria:
* Is the documentation complete and precise? (1-5)
* Does it improve understanding of the project or module? (1-5)
* Is the formatting and style consistent? (1-5)Scale: 1-5 (where 5 represents thorough and clear documentation).
5. TestsDescription: Commits adding, modifying, or removing unit, integration, or other tests.Evaluation Criteria:
* Are the tests well-written and effectively covering functionality? (1-10)
* Do they account for edge cases? (1-5)
* Are they consistent with project conventions? (1-5)Scale: 1-10 (where 10 represents a comprehensive and thoughtful test implementation).
6. OptimizationDescription: Commits improving application performance.Evaluation Criteria:
* How significant are the benefits of the optimization? (1-10)
* Do the changes avoid causing regression in functionality? (1-5)
* Is the optimization aligned with best practices? (1-5)Scale: 1-10 (where 10 represents significant benefits without negative impact).
7. Configuration/DevOpsDescription: Commits modifying configuration files, CI/CD scripts, Dockerfiles, etc.Evaluation Criteria:
* Do the changes improve development or deployment processes? (1-5)
* Do they avoid introducing potential configuration issues? (1-5)
* Are they well-documented? (1-5)Scale: 1-5 (where 5 represents flawless configuration).
8. Technical Debt ReductionDescription: Commits that remove outdated code, reduce complexity, etc.Evaluation Criteria:
* Does it reduce code complexity? (1-5)
* Does it remove unnecessary dependencies or code? (1-5)
* Do the changes improve long-term project quality? (1-5)Scale: 1-5 (where 5 represents complete elimination of technical debt).
9. UI/UX ChangesDescription: Commits introducing changes to the user interface.Evaluation Criteria:
* Do the changes improve user experience? (1-5)
* Is the interface consistent with project guidelines? (1-5)
* Are visual or regression tests included? (1-5)Scale: 1-5 (where 5 represents significant and positive changes).
10. Experimental/Proof of ConceptDescription: Commits introducing experimental features or testing new approaches.Evaluation Criteria:
* Are the changes clearly marked as experimental? (1-3)
* Do they achieve the experiment's purpose? (1-5)
* Can they be easily adapted into the main project? (1-5)Scale: 1-5 (where 5 represents a successful experiment).
"""
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
                    print(files_before_new_commit)
                    print("****************************************************************************************")
                    print(files_new)
                    # prompt = f"Compare these two files for me. Files before new commit {files_before_new_commit}.Changed files after new commit {files_new}. Match them to the category and evaluate according to the given criteria"
                    # prompt = f"""Based on those cryteria {evaluation_criteria} evaluate and categorize commits into difrent commit category. 
                    #     You will get files after and before new commit.
                    #     Files before new commit {files_before_new_commit}. Changed files after new commit {files_new}"""
                    # output = connect_to_llama(prompt_message=prompt)
                    # for i in range(len(files_new)):
                    prompt1 = f"Compare these two files for me (code in those files). Match them to the 1 of 10 categories based on {evaluation_criteria} and evaluate according to the given criteria."
                    prompt2 = f"Files before new commit: {files_before_new_commit}.Changed files after new commit {files_new}."
                    output = connect_to_llama(prompt_message=prompt1)
                    output = connect_to_llama(prompt_message=prompt2)
                    # for file in files_new:
                    #     output = connect_to_llama(prompt_message=prompt)
                else:
                    continue

    except Exception as e:
        print(f"Błąd: {e}")

print("DUPADUPADUPADUPADUPADUPADUPADUPADUPADUPADUPADUPADUPA")

# prompt = f""" You will receive the same files before and after the new commit. Your task is to compare them and write a detailed report on what has been added to each file individually.
#                         Categorize the changes introduced in the commit according to the following criteria:
#                         Commit Categories, Scales, and Evaluation Criteria
#                         1. Bug Fixes
#                         Description: Commits in this category address existing bugs in the code.
#                         Evaluation Criteria:
#                         Does the fix fully resolve the issue? (1-5)
#                         Are the changes minimal and precise? (1-5)
#                         Does the fix avoid introducing new potential bugs? (1-5)
#                         Scale: 1-5 (where 5 represents the highest quality fix).
#                         2. Feature Additions
#                         Description: Commits introducing new features or components.
#                         Evaluation Criteria:
#                         How well is the feature implemented? (1-10)
#                         Is the code modular and easy to extend? (1-5)
#                         Are adequate tests provided for the new feature? (1-5)
#                         Scale: 1-10 (where 10 represents a fully thought-out and comprehensive implementation).
#                         3. Code Refactoring
#                         Description: Commits that restructure code without adding new features.
#                         Evaluation Criteria:
#                         Does the refactoring improve code readability? (1-5)
#                         Does it enhance performance or scalability? (1-5)
#                         Does it preserve existing functionality? (1-5)
#                         Scale: 1-5 (where 5 represents flawless execution).
#                         4. Documentation Updates
#                         Description: Commits related to documentation, e.g., README files or code comments.
#                         Evaluation Criteria:
#                         Is the documentation complete and precise? (1-5)
#                         Does it improve understanding of the project or module? (1-5)
#                         Is the formatting and style consistent? (1-5)
#                         Scale: 1-5 (where 5 represents thorough and clear documentation).
#                         5. Tests
#                         Description: Commits adding, modifying, or removing unit, integration, or other tests.
#                         Evaluation Criteria:
#                         Are the tests well-written and effectively covering functionality? (1-10)
#                         Do they account for edge cases? (1-5)
#                         Are they consistent with project conventions? (1-5)
#                         Scale: 1-10 (where 10 represents a comprehensive and thoughtful test implementation).
#                         6. Optimization
#                         Description: Commits improving application performance.
#                         Evaluation Criteria:
#                         How significant are the benefits of the optimization? (1-10)
#                         Do the changes avoid causing regression in functionality? (1-5)
#                         Is the optimization aligned with best practices? (1-5)
#                         Scale: 1-10 (where 10 represents significant benefits without negative impact).
#                         7. Configuration/DevOps
#                         Description: Commits modifying configuration files, CI/CD scripts, Dockerfiles, etc.
#                         Evaluation Criteria:
#                         Do the changes improve development or deployment processes? (1-5)
#                         Do they avoid introducing potential configuration issues? (1-5)
#                         Are they well-documented? (1-5)
#                         Scale: 1-5 (where 5 represents flawless configuration).
#                         8. Technical Debt Reduction
#                         Description: Commits that remove outdated code, reduce complexity, etc.
#                         Evaluation Criteria:
#                         Does it reduce code complexity? (1-5)
#                         Does it remove unnecessary dependencies or code? (1-5)
#                         Do the changes improve long-term project quality? (1-5)
#                         Scale: 1-5 (where 5 represents complete elimination of technical debt).
#                         9. UI/UX Changes
#                         Description: Commits introducing changes to the user interface.
#                         Evaluation Criteria:
#                         Do the changes improve user experience? (1-5)
#                         Is the interface consistent with project guidelines? (1-5)
#                         Are visual or regression tests included? (1-5)
#                         Scale: 1-5 (where 5 represents significant and positive changes).
#                         10. Experimental/Proof of Concept
#                         Description: Commits introducing experimental features or testing new approaches.
#                         Evaluation Criteria:
#                         Are the changes clearly marked as experimental? (1-3)
#                         Do they achieve the experiment's purpose? (1-5)
#                         Can they be easily adapted into the main project? (1-5)
#                         Scale: 1-5 (where 5 represents a successful experiment).
#                         The final response should look like this, for example:
#                         Summary
#                         Main commit category: Feature Additions.
#                         Overall rating: 7/10. Files before new commit {files_before_new_commit}. Changed files after new commit {files_new}"""