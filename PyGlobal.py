import time
import importlib
import requests
import json
from colorama import Fore, Style

def install_package(package):
    try:
        importlib.import_module(package)
        print(f"{package} is already installed.")
    except ImportError:
        try:
            import pip
            print(f"Installing {package}...")
            pip.main(['install', package])
            print(f"{package} has been installed successfully.")
        except:
            print(f"Failed to install {package}. Make sure you have pip installed.")

def show_progress_percentage(progress):
    bar = "[" + Fore.GREEN + "|" * (progress // 2) + " " * (50 - progress // 2) + "]" + Style.RESET_ALL
    percentage = f"{progress}%"
    print(f"\r{bar} {percentage}", end="")

def check_package_installation(packages):
    total_packages = len(packages)
    installed_packages = 0

    for package in packages:
        try:
            importlib.import_module(package)
            installed_packages += 1
        except ImportError:
            install_package(package)

    if installed_packages == total_packages:
        print(Fore.GREEN + "All packages are installed.")
    else:
        print(Fore.YELLOW + "Package installation complete.")

def show_program_loading():
    print("Loading pyglobal:")
    for i in range(11):
        time.sleep(1)
        show_progress_percentage(i * 10)
    print("\nUpdating Important Files!")
    time.sleep(5)
    print("Update complete.")

def mention_user(user_id):
    return f"<@{user_id}>"

def get_user_information(user_id):
    response = requests.get(f"https://discord.com/api/v9/users/{user_id}")
    if response.status_code == 200:
        data = response.json()
        username = data.get("username")
        discriminator = data.get("discriminator")
        created_at = data.get("created_at")
        avatar_id = data.get("avatar")
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}.png" if avatar_id else None

        return username, discriminator, created_at, avatar_url

    return None

def send_embed(webhook, message, name, image_url=None, mention=None):
    embed = {
        "title": f"Message by: {name}",
        "description": message,
        "footer": {
            "text": "By Alex • PYGlobal"
        }
    }

    if image_url is not None and image_url.strip():
        embed["footer"]["icon_url"] = image_url.strip()

    payload = {
        "content": message,
        "embeds": [embed]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(webhook, data=json.dumps(payload), headers=headers)

    if response.status_code == 204:
        print("Embed sent successfully.")
    else:
        print("Error sending the embed. Check the webhook and try again.")

# Check and install the required packages
required_packages = ["colorama", "requests"]

print("Checking package installation...")
check_package_installation(required_packages)

# Show program loading
show_program_loading()

# Show the menu options
print("\n--- PYGlobal Tool ---")
print("[1] Send a message to a webhook")
print("[2] Get information from a Discord ID")

option = input("Select an option: ")

if option == "1":
    print("\n--- Send a message to a webhook ---")
    webhook = input(Fore.YELLOW + "Webhook: ")
    name = input(Fore.YELLOW + "Your Name: ")
    message = input(Fore.YELLOW + "Message: ")
    image_url = input(Fore.YELLOW + "Image URL (optional): ")

    # Check if a user mention is desired
    mention_user_option = input(Fore.YELLOW + "Do you want to mention a user? (y/n): ")
    mention = None
    if mention_user_option.lower() == "y":
        user_id = input(Fore.YELLOW + "User ID to mention: ")
        mention = mention_user(user_id)

    # Send the embed
    send_embed(webhook, message, name, image_url, mention)
elif option == "2":
    print("\n--- Get information from a Discord ID ---")
    user_id = input(Fore.YELLOW + "ID to inspect: ")
    webhook = input(Fore.YELLOW + "Webhook (for the embed): ")

    # Get user information
    user_info = get_user_information(user_id)
    if user_info is not None:
        username, discriminator, created_at, avatar_url = user_info

        embed = {
            "title": "User Information",
            "fields": [
                {"name": "User", "value": f"{username}#{discriminator}"},
                {"name": "ID", "value": user_id},
                {"name": "Creation Date", "value": created_at}
            ],
            "footer": {
                "text": "By Alex • PYGlobal"
            }
        }

        if avatar_url is not None:
            embed["thumbnail"] = {"url": avatar_url}

        payload = {
            "content": "",
            "embeds": [embed]
        }

        headers = {
            "Content-Type": "application/json"
        }

        response = requests.post(webhook, data=json.dumps(payload), headers=headers)

        if response.status_code == 204:
            print("Embed sent successfully.")
        else:
            print("Error sending the embed. Check the webhook and try again.")
    else:
        print("Failed to retrieve user information.")
else:
    print("Invalid option.")
