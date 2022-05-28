from selenium import webdriver
from selenium.webdriver.common.by import By

from webdriver_manager.chrome import ChromeDriverManager

from pprint import pprint


def generate_url(region, category, position=None):
    if category == 'champions':
        url = f'https://{region}.op.gg/champions?position={position}'
    elif category == 'leaderboards':
        url = f'https://{region}.op.gg/leaderboards/tier?region={region}'
    else:
        raise ValueError('Category can only be "champions" or "leaderboards"')
    return url

url = generate_url('euw', 'leaderboards')

driver = webdriver.Chrome(ChromeDriverManager().install())



def scrape(pages=1):
    # for leaderboards category you can pass how much pages of leaderboard you want to scrap data from

    result = [] 
    
    if 'champions' in url: 
        driver.get(url)
        
        champions_names = driver.find_elements(by=By.CLASS_NAME, value='css-1q252wa')
        champions_tiers = driver.find_elements(by=By.CLASS_NAME, value='css-ew1afn')
        champions_rates = driver.find_elements(by=By.CLASS_NAME, value='css-1wvfkid')

        win_rate_idx = 0
        pick_rate_idx = 1
        ban_rate_idx = 2

        for name, tier in zip(champions_names, champions_tiers):
            
            win_rate = champions_rates[win_rate_idx].text
            pick_rate = champions_rates[pick_rate_idx].text
            ban_rate = champions_rates[ban_rate_idx].text

            champion = {
                'Name': name.text,
                'Tier': tier.text,
                'Win_rate': win_rate,
                'Pick_rate': pick_rate,
                'Ban_rate': ban_rate
            }

            win_rate_idx += 3
            pick_rate_idx += 3
            ban_rate_idx += 3

            result.append(champion)

    
    else:
        page = 1

        while page <= pages:

            page_url = url + f'&page={page}'
            driver.get(page_url)

            players_names = driver.find_elements(by=By.CLASS_NAME, value='css-pybncm')
            players_ranks = driver.find_elements(by=By.CLASS_NAME, value='css-kwucg')
            players_LPs_levels = driver.find_elements(by=By.CLASS_NAME, value='css-j6nsb0')
            
            player_LP_idx = 0
            player_level_idx = 1

            players_win_rates = driver.find_elements(by=By.CLASS_NAME, value='css-1s4dslc')
            
            for name, rank in zip(players_names, players_ranks):
                
                lp = players_LPs_levels[player_LP_idx].text
                level = players_LPs_levels[player_level_idx].text

                player = {
                    'Name': name.text,
                    'Rank': rank.text,
                    'LP': lp,
                    'Level': level,
                }

                player_LP_idx += 2
                player_level_idx += 2

                result.append(player)
            page += 1

    return result


pprint(scrape(2))