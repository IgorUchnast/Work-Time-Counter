from ollama import AsyncClient
import requests
import asyncio 

BASE_URL = "http://127.0.0.1:5000"
async def chat(msg,hint_msg):
    """
    Stream a chat from Llama using the AsyncClient.
    """
    message = {
        "role": "user",
        "content": f"{hint_msg} Data: {msg}"
        # "content" : f"{msg}",
        # "content": f"You are goig to get a data about an eployee {employee_id} projects. Data: {msg}"
    }
    async for part in await AsyncClient().chat(
        model="llama3", messages=[message], stream=True
    ):
        print(part["message"]["content"], end="", flush=True)




def get_data(url):
    try:
        # Wykonaj zapytanie GET do endpointu
        response = requests.get(url)

        # Sprawdź, czy odpowiedź jest poprawna (status 200)
        if response.status_code == 200:
            # Zwróć dane w formacie JSON
            return response.json()
        else:
            print(f"Błąd: Nie udało się pobrać danych. Status: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Błąd połączenia: {e}")
        return None
    

employee_id = 0
project_id = 0
urls = [
    f"{BASE_URL}/projects",
    f"{BASE_URL}/project/{project_id}/members",
    f"{BASE_URL}/project/{project_id}/tasks",
    f"{BASE_URL}/employees",
    f"{BASE_URL}/employee/{employee_id}/taks", 
    f"{BASE_URL}/employee/{employee_id}/projects", 
]
    
hint_msg = [
    f"You are goig to get a data about an all projects",
    f"You are goig to get a data about an all employees",
    f"You are goig to get a data about an eployee {employee_id} projects",
    f"You are goig to get a data about an eployee {employee_id} task_assignments",
]

msg = input("Start/Exit : ")

if msg == "Start":
    while msg != "Exit":
        msg = input("Chose data that you want to anylize projects/employees? : ")
        if msg == "projects":
             msg = input("AllProjects?\nProjectID/Members?\nProjectID/Task?\n")
             if msg == "AllProjects?":
                projects = get_data(urls[0])
                if projects:
                    projects_data = ""
                    for project in projects:
                        projects_data += f"ID: {project['project_id']},\nTytuł: {project['title']},\nOpis: {project['description']},\nData rozpoczęcia: {project['start_date']},\nLider ID: {project['leader_id']}"
                    asyncio.run(chat(msg=projects_data, hint_msg=hint_msg[0]))
                else:
                    print("Brak danych.")
             elif msg == "ProjectID/Members":
                project_members = get_data(urls[1])
             elif msg == "ProjectID/Task":
                project_tasks = get_data(urls[2])
        if msg == "projects":
             msg = input("AllEmployees?\nEmployeeID/Projects?\nEmployeeID/Tasks?\n")
             if msg == "AllEmployees?":
                employees = get_data(urls[3])
             elif msg == "EmployeeID/Projects":
                employee_projects = get_data(urls[4])
             elif msg == "EmployeeID/Tasks":
                employee_tasks = get_data(urls[5])
# asyncio.run(chat(msg="DUPA"))

# if projects:
#     for project in projects:
#         print(f"ID: {project['project_id']}, Tytuł: {project['title']}, Opis: {project['description']}, Data rozpoczęcia: {project['start_date']}, Lider ID: {project['leader_id']}")
# else:
#     print("Brak danych.")