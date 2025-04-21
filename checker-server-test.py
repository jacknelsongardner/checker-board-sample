import requests

# Base URL of the Flask server
BASE_URL = "http://localhost:2000"

# Test initialize
print("Testing /initialize")
response = requests.get(f"{BASE_URL}/initialize")
print(response.json())

# Test a move (random example move)
print("Testing /move")

move_data = {
    "x_old": 2,
    "y_old": 5,
    "x_new": 3,
    "y_new": 4,
    "color": 1,
    "board": response.json()['board']  # use the board from the initialize response
}

response = requests.post(f"{BASE_URL}/move", json=move_data)
print(response.json())
