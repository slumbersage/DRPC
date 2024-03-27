# Discord Presence Updater with Dynamic Icons

Welcome to our Python script that updates your Discord presence with dynamic icons based on the currently focused application window.

## Features
- **Dynamic Presence**: The script monitors your focused window and updates your Discord presence accordingly, displaying the application you're currently using.
- **Personalized Icons**: Icons are fetched from the web based on the focused application's name, providing a unique presence for each application.
- **Randomized Icons**: Special application names receive randomized icon URLs, adding variety to your Discord status.

## How It Works
1. **Window Monitoring**: The script tracks your currently focused window on your desktop.
2. **Icon Fetching**: It extracts the application name from the window title and fetches an icon from the web based on the application name.
3. **Discord Presence Update**: The script updates your Discord presence with the fetched icon and relevant details, providing real-time insights into your activities.
4. **Please note that this code currently works on linux systems only.**
## Setup
1. **Dependencies**: Ensure you have Python 3.x installed along with the required dependencies listed in `requirements.txt`.
2. **Discord Client ID**: Replace `'your_client_id'` in the script with your actual Discord client ID.
3. **Running the Script**: Execute `python3 DRPC.py` to start updating your Discord presence with dynamic icons.

## Customization
- **Special Application Names**: Customize the `special_names` list in the script to include your preferred special application names for randomized icons.
- **Update Frequency**: Adjust the update frequency in the script to control how often your Discord presence gets updated.

## Contributions
Contributions are welcomed! Feel free to fork this repository, make improvements, and submit a pull request. Let's enhance this script for everyone to enjoy.

## Credits
Crafted by altin & aiko, inspired by the desire to personalize Discord presence with dynamic icons.
