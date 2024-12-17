"""
Pobranie danych z githuba od nośnie commitow i repozytoriow oraz nowych w pklikach zmian:
-> Wysyłanie zaoyatania GET co 2 minuty do GithubAPI 
-> Analiza nowo dodanych commitów porównanie ich czy jest jakiś nowy: 
    -> Jeśli jest:
        -> Analiza commita: 
            -> Wiadomość commita
            -> Data stworzenia i zatwierdzenia commita
            -> Lista zmienionych plików, ich status (added, modified, removed).
            -> Szczegóły zmian (np. liczba dodanych/usuniętych linii, diff w formacie patch).
            -> Endpointy:
                -> GET /repos/{owner}/{repo}/commits – Lista commitów w repozytorium.
                -> GET /repos/{owner}/{repo}/commits/{sha} – Szczegóły konkretnego commita.
        -> 
    -> Jeśli nie jest:
        -> Nic się nie dzieje. Program leci dalej
-> Analiza szybkości rozwiązywania problemów przez poszczególnych pracowników w 
    -> Tytuł, opis, status (open/closed)
    -> Twórca, przypisane osoby, data utworzenia/zamknięcia
    -> Ocena Komentarzy i ich treści
    -> Endpointy:
        -> GET /repos/{owner}/{repo}/issues – Lista issues w repozytorium.
        -> GET /repos/{owner}/{repo}/issues/{issue_number} – Szczegóły konkretnego issue.
-> Analiza plikow w repozytorium:
    -> Dostęp do plików::
        -> Zawartość pliku w formacie base64
        -> Historia zmian w plikach (commity dotyczące danego pliku)
    -> Endpointy:
        -> GET /repos/{owner}/{repo}/contents/{path} – Pobranie pliku/zawartości folderu
        -> GET /repos/{owner}/{repo}/commits?path={path} – Lista commitów dotyczących konkretnego pliku
-> Statystyki i analiza
    -> Statystyki repozytorium:
        -> Wkład poszczególnych użytkowników (ilość commitów, dodanych/usuniętych linii).
        -> Historia commitów na przestrzeni czasu.
    -> Statystyki aktywności w issues i pull requestach.
    -> Endpointy:
        -> GET /repos/{owner}/{repo}/stats/contributors – Wkład użytkowników.
        -> GET /repos/{owner}/{repo}/stats/commit_activity – Aktywność commitów.
"""

import ollama 
# from ollama import AsyncClient
import requests
import asyncio 

BASE_URL = "http://127.0.0.1:5000"

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

# , hint_info
# def connect_to_llama(prompt_message, prompt_data):
#     reposne = ollama.chat(
#         model='llama3', messages=[
#             {
#                 'role':'user',
#                 'content': f"Infomracja na temat sposobu w jaki chcę uzyskać odpowiedź: {prompt_message}: 
#                 Dane, za pomocą, których masz mi odpowiedzieć:  {prompt_data}",
#             },
#         ])

#     print(reposne['message']['content'])

def connect_to_llama(prompt_message, prompt_data):
    # Wywołanie funkcji ollama.chat z poprawnym formatem wiadomości
    response = ollama.chat(
        model='llama3', 
        messages=[
            {
                'role': 'user',
                'content': f"""Informacja na temat sposobu, w jaki chcę uzyskać odpowiedź: {prompt_message}
Dane, za pomocą których masz mi odpowiedzieć: {prompt_data}"""
            },
        ]
    )
    
    # Sprawdzenie struktury odpowiedzi
    if 'message' in response and 'content' in response['message']:
        print(response['message']['content'])
    else:
        print("Błąd: Nie znaleziono wiadomości w odpowiedzi.")

# Przykładowe wywołanie funkcji
# connect_to_llama("Proszę o podsumowanie", "Dane do analizy...")

