# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
import json
from api_key import API_KEY, TOKEN, BASE_URL

url = f"{BASE_URL}/lists/6730be275f5fd85a45f704f2/cards"

headers = {
  "Accept": "application/json"
}

query = {
  'key': API_KEY,
  'token': TOKEN
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# url = f"{BASE_URL}/members/6365183f34ef3003c61c1011/cards"

# headers = {
#   "Accept": "application/json"
# }

# query = {
#   'key': 'API_KEY',
#   'token': 'TOKEN'
# }

# response = requests.request(
#    "GET",
#    url,
#    headers=headers,
#    params=query
# )

# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

# def get_trello_cards(list_id):
    
#     url = f"{BASE_URL}/lists/{list_id}/cards"
#     params = {
#         'key': API_KEY,
#         'token': TOKEN
#     }

#     response = requests.get(url, params=params)
    
#     # Sprawdzenie, czy zapytanie się powiodło
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Błąd: {response.status_code}")
#         return None
    

# dupa = get_trello_cards("6730be275f5fd85a45f704f2")
# # print(dupa)


# import requests
# import json

# url = f"{BASE_URL}/members/672dfa615c4a73514c825acd/cards"

# headers = {
#   "Accept": "application/json"
# }

# query = {
#   'key': API_KEY,
#   'token': TOKEN
# }

# response = requests.request(
#    "GET",
#    url,
#    headers=headers,
#    params=query
# )

# print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))