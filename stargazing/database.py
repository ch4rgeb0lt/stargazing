import json
from pathlib import Path

# Path to the JSON file
DATA_PATH = Path(__file__).parent / "database" / "users.json"

def load_data():
    if not DATA_PATH.exists():
        return {"users": []}

    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"users": []}


# SAVE DATA
def save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


# ADD NEW USER
def add_user(username, email):
    data = load_data()

    # Check for duplicates
    if any(user["email"] == email for user in data["users"]):
        raise ValueError(f"User with email '{email}' already exists.")

    # Add new user with empty location
    data["users"].append({
        "username": username,
        "email": email,
        "location": None
    })

    save_data(data)


# CHECK IF USER EXISTS
def user_exists(email):
    data = load_data()
    return any(user["email"] == email for user in data["users"])


# Update location 
def set_user_location(email, location):
    data = load_data()
    updated = False

    for user in data["users"]:
        if user["email"] == email:
            user["location"] = location
            updated = True
            break

    if not updated:
        raise ValueError(f"No user found with email '{email}'")

    save_data(data)


# GET INFO 
def get_user(email):
    data = load_data()
    for user in data.get("users", []):
        if user.get("email") == email:
            return (user.get("email"), user.get("location", "Unknown"))
    return (None, None)
