import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

start_time = time.time()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}

# Initialize a list to store team data for all seasons
all_team_data = []

# Define the range of seasons from 1950 to 2023 (you can adjust this range as needed)
seasons = range(2000, 2024)

for season in seasons:
    # Construct the URL for the specific season
    page = f"https://www.transfermarkt.de/ligue-1/startseite/wettbewerb/FR1/plus/?saison_id={season}"
    pageTree = requests.get(page, headers=headers)
    
    # Set the encoding to UTF-8
    #pageTree.encoding = 'utf-8'
    
    pageSoup = BeautifulSoup(pageTree.text, 'html.parser')

    teamLinks = []
    team_data = []  # Store team data for the current season

    buli_team_elements = pageSoup.find_all(class_="hauptlink no-border-links")

    for buli_team_element in buli_team_elements:
        # Extract team_links data here
        team_link = buli_team_element.find("a").get("href")
        teamLinks.append(team_link)

    for team_link in teamLinks:
        team_url = "https://www.transfermarkt.de" + team_link
        team_page = requests.get(team_url, headers=headers)
        
        # Set the encoding to UTF-8
        #team_page.encoding = 'utf-8'
        
        team_soup = BeautifulSoup(team_page.text, 'html.parser')

        # Get team name
        team = team_soup.find(class_="data-header__headline-wrapper--oswald")
        team_name = team.text.strip()

        # Get player names
        players = team_soup.find_all('img', {"class": "bilderrahmen-fixed lazy lazy"})

        player_names = [player.get('alt') for player in players]

        # Append team data as a tuple (season, team_name, player_names) to the team_data list
        team_data.append((season, team_name, player_names))

    # Append team data for the current season to the all_team_data list
    all_team_data.extend(team_data)

# Create a pandas DataFrame from the all_team_data list
df = pd.DataFrame(all_team_data, columns=['Season', 'Team', 'Player Names'])

# Save the DataFrame to a CSV file with UTF-8 encoding
df.to_csv('ligue1_players_by_season.csv', index=False, encoding='utf-8-sig')

# Print the DataFrame
print(df)

end_time = time.time()
runtime = end_time - start_time
minutes, seconds = divmod(runtime, 60)
print(f"Runtime: {int(minutes)} minutes and {int(seconds)} seconds")
