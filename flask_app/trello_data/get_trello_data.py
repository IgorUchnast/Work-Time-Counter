from config.api_key import API_KEY, TOKEN, BASE_URL, WORK_SPACE
import requests

def get_boards_in_workspace(workspace_id): 
    url = f"{BASE_URL}/organizations/{workspace_id}/boards"
    params = {
        'key': API_KEY,
        'token': TOKEN
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}")
        return None

def get_trello_data(board_id, data_type):

    url = f"{BASE_URL}/boards/{board_id}/{data_type}"
    params = {
        'key': API_KEY,
        'token': TOKEN
    }

    response = requests.get(url, params=params)
    
    # Sprawdzenie, czy zapytanie się powiodło
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}")
        return None
    
def get_trello_member_cards(member_id):
    
    url = f"{BASE_URL}/members/{member_id}/cards"
    params = {
        'key': API_KEY,
        'token': TOKEN
    }

    response = requests.get(url, params=params)
    
    # Sprawdzenie, czy zapytanie się powiodło
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}")
        return None
    
def get_trello_cards(list_id):
    
    url = f"{BASE_URL}/lists/{list_id}/cards"
    params = {
        'key': API_KEY,
        'token': TOKEN
    }

    response = requests.get(url, params=params)
    
    # Sprawdzenie, czy zapytanie się powiodło
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Błąd: {response.status_code}")
        return None