import json
import os
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

# File to store account details
ACCOUNTS_FILE = "accounts.json"

# Load existing accounts
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    return {}

# Save accounts
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

# Display menu
def show_menu():
    print("\n🔹 Telegram Multi-Account Management 🔹")
    print("1️⃣ Add New Telegram Account")
    print("2️⃣ List Logged-in Accounts")
    print("3️⃣ Access an Account")
    print("4️⃣ Remove an Account")
    print("5️⃣ Show Login/Logout History")
    print("6️⃣ Exit")
    return input("\nChoose an option: ")

# Add a new Telegram account
def add_account():
    api_id = int(input("Enter API ID: "))
    api_hash = input("Enter API Hash: ")
    phone_number = input("Enter Phone Number: ")

    client = TelegramClient(f"session_{phone_number}", api_id, api_hash)
    client.connect()

    if not client.is_user_authorized():
        try:
            client.send_code_request(phone_number)
            client.sign_in(phone_number, input("Enter OTP: "))
        except SessionPasswordNeededError:
            password = input("Enter your 2FA password: ")
            client.sign_in(password=password)

    accounts = load_accounts()
    accounts[phone_number] = {"api_id": api_id, "api_hash": api_hash}
    save_accounts(accounts)
    print(f"✅ {phone_number} added successfully!")

# List logged-in accounts
def list_accounts():
    accounts = load_accounts()
    if not accounts:
        print("⚠️ No accounts logged in.")
    else:
        print("\n🔹 Logged-in Accounts:")
        for idx, phone in enumerate(accounts.keys(), 1):
            print(f"{idx}. {phone}")

# Access a specific account
def access_account():
    accounts = load_accounts()
    if not accounts:
        print("⚠️ No accounts available.")
        return

    list_accounts()
    choice = int(input("\nSelect account number: ")) - 1
    phone = list(accounts.keys())[choice]

    client = TelegramClient(f"session_{phone}", accounts[phone]["api_id"], accounts[phone]["api_hash"])
    client.connect()

    while True:
        print(f"\n🔹 Managing Account: {phone}")
        print("1️⃣ Read Last 5 OTP Messages")
        print("2️⃣ Start New Chat")
        print("3️⃣ Logout")
        print("4️⃣ Back to Main Menu")
        action = input("\nChoose an option: ")

        if action == "1":
            messages = client.get_messages(777000, limit=5)
            for msg in messages:
                print(f"🔹 OTP: {msg.text}")
        elif action == "2":
            user = input("Enter username/phone/user ID: ")
            message = input("Enter message: ")
            client.send_message(user, message)
            print("✅ Message sent!")
        elif action == "3":
            client.log_out()
            print("✅ Logged out successfully!")
            break
        elif action == "4":
            break

# Remove an account
def remove_account():
    accounts = load_accounts()
    if not accounts:
        print("⚠️ No accounts to remove.")
        return

    list_accounts()
    choice = int(input("\nSelect account number to remove: ")) - 1
    phone = list(accounts.keys())[choice]

    os.remove(f"session_{phone}.session")
    del accounts[phone]
    save_accounts(accounts)
    print(f"✅ {phone} removed successfully!")

# Show login/logout history (Mock Data)
def show_history():
    print("\n🔹 Login/Logout History:")
    print("📅 [2025-03-10] Account +919649456601 logged in")
    print("📅 [2025-03-09] Account +919649456602 logged out")

# Main loop
while True:
    option = show_menu()
    if option == "1":
        add_account()
    elif option == "2":
        list_accounts()
    elif option == "3":
        access_account()
    elif option == "4":
        remove_account()
    elif option == "5":
        show_history()
    elif option == "6":
        print("👋 Exiting... Goodbye!")
        break
    else:
        print("⚠️ Invalid option, please try again.")
