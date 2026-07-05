from cryptography.fernet import Fernet
import json
import os
from getpass import getpass

KEY_FILE = "secret.key"
DATA_FILE = "passwords.json"

def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
    with open(KEY_FILE, "rb") as f:
        return f.read()

key = load_key()
cipher = Fernet(key)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

while True:
    print("\n===== PASSWORD MANAGER =====")
    print("1. Add Password")
    print("2. View Password")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        website = input("Website: ")
        username = input("Username: ")
        password = getpass("Password: ")

        encrypted = cipher.encrypt(password.encode()).decode()

        data = load_data()
        data[website] = {
            "username": username,
            "password": encrypted
        }

        save_data(data)
        print("Password Saved Successfully!")

    elif choice == "2":
        website = input("Website: ")

        data = load_data()

        if website in data:
            decrypted = cipher.decrypt(
                data[website]["password"].encode()
            ).decode()

            print("\nUsername:", data[website]["username"])
            print("Password:", decrypted)
        else:
            print("Website not found!")

    elif choice == "3":
        break

    else:
        print("Invalid Choice!")