import subprocess
import re
import time
import requests
import json
import random
from pypresence import Presence
import urllib

base_url = "https://cdn.iconscout.com/"

# List of special application names that should have randomized icon URLs
special_names = ["@discord", "#rules", "#general", "@"]

# Function to get the title of the currently focused window
def get_focused_window_title():
    try:
        window_id = subprocess.run(["xdotool", "getwindowfocus"], capture_output=True, text=True).stdout.strip()
        window_info = subprocess.run(["xprop", "-id", window_id], capture_output=True, text=True)
        title_line = [line for line in window_info.stdout.split('\n') if "WM_NAME" in line][0]
        title = title_line.split('=', 1)[1].strip().strip('"')
        return title
    except Exception as e:
        print(f"Error getting window title: {e}")
        return "Unknown"

# Function to fetch icons from a given URL
def fetch_icons(url, app_name, stored_urls):
    # Remove special characters from app name
    app_name = re.sub(r'[#@]', '', app_name)

    print("Fetching URL:", url)  # Print URL for debugging

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Use regular expressions to find the URLs
        pattern = r'src="(' + re.escape(base_url) + r'.*?)"'
        urls = re.findall(pattern, response.text)

        # For special names, randomize the URL and always update
        if app_name.lower() in special_names:
            random.shuffle(urls)
            stored_urls[app_name] = urls[0] if urls else None
        else:
            # Update only if not already stored
            stored_urls.setdefault(app_name, urls[0] if urls else None)

        # Overwrite the existing JSON file with the updated stored URLs
        with open("stored_urls.json", "w") as f:
            json.dump(stored_urls, f, indent=4)

        return stored_urls[app_name]
    else:
        print("Failed to fetch the page:", response.status_code)  # Print error status code
        return None

# Function to update Discord presence
def update_discord_presence():
    client_id = 'your_client_id'  # Replace 'your_client_id' with your actual client ID
    RPC = Presence(client_id)
    RPC.connect()

    # Load stored URLs from file if exists, otherwise initialize an empty dictionary
    try:
        with open("stored_urls.json", "r") as f:
            stored_urls = json.load(f)
    except FileNotFoundError:
        stored_urls = {}

    while True:
        focused_window_title = get_focused_window_title()

        # Extract application name from window title
        match = re.search(r'^(.*?)\s*-\s*(.*?)\s*-\s*(.*?)$', focused_window_title)
        if match:
            app_name = match.group(3).strip()
        else:
            app_name = focused_window_title

        # Encode the application name to ensure it's in URL format
        encoded_app_name = urllib.parse.quote(app_name.lower().replace(' ', '-'), safe='')

        # Define the URL to scrape based on the application name
        url = f"https://iconscout.com/icons/{encoded_app_name}"

        # Fetch the icon from the given URL
        icon_url = fetch_icons(url, app_name, stored_urls)

        # Truncate state if it exceeds 128 characters
        state = f"Focused on: {focused_window_title}"
        if len(state) > 128:
            state = state[:125] + "..."

        presence_data = {
            'details': "Using my computer",
            'state': state,
            'large_image': icon_url or None,
            'large_text': focused_window_title or None,
            'small_image': icon_url or None,
            'small_text': "@slumbersage",
            'buttons': [
                {"label": "Button 1", "url": "https://example.com"},
                {"label": "Join Discord", "url": "https://discord.gg/MqkWAReHq7"}
            ]
        }

        print("Presence Data:", presence_data)  # Print presence data for debugging
        RPC.update(**presence_data)
        time.sleep(3)  # Update every 3 seconds

if __name__ == "__main__":
    update_discord_presence()
