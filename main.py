from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
import helpers
from selenium.webdriver.common.by import By

# Instantiate Webdriver


option = webdriver.ChromeOptions()
option.add_argument("— incognito")

username = "zoybot"
password = "RobotRobot"

browser = webdriver.Chrome(
    executable_path='/usr/lib/chromium-browser/chromedriver', chrome_options=option)


def getWeather():
    whole = browser.find_element(By.XPATH,'/html')
    htmldata = whole.get_attribute("innerHTML")
    html = str(htmldata)
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.prettify()
    soupstring = str(soup)

    lines = soupstring.split("\n")
    for k in range(0, len(lines)):
        if '<div class=\"weather\">' in lines[k]:
            if '<em>' in lines[k+3] and '</em>' in lines[k+4]:
                return "none"
            else:
                m = k + 1
                while "<" in lines[m]:
                    m = m + 1
                return lines[m].strip()


page = browser.get("https://play.pokemonshowdown.com/")
time.sleep(2)

# login
loginbox = browser.find_element(By.XPATH, "/html/body/div[1]/div[3]/button[1]")
loginbox.click()

userbox = browser.find_element(By.NAME, "username")
userbox.send_keys(username)
userbox.send_keys(Keys.ENTER)

time.sleep(.55)

passwordbox = browser.find_element(By.NAME, "password")
passwordbox.send_keys(password)
passwordbox.send_keys(Keys.ENTER)

input("Press Enter to continue...")

# scraping your team Data
for k in range(1, 7):
    action = ActionChains(browser)
    xpath = "/html/body/div[4]/div[5]/div/div[3]/div[2]/button[" + str(k) + "]"
    firstLevelMenu = browser.find_element(By.XPATH, xpath)
    action.move_to_element(firstLevelMenu).perform()

    time.sleep(.5)

    whole = browser.find_element(By.XPATH, '/html')
    htmldata = whole.get_attribute("innerHTML")
    html = str(htmldata)
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.prettify()
    soupstring = str(soup)

    filename = "pokemon" + str(k) + "data.txt"
    file = open(filename, 'w')
    file.write(soupstring)
    file.close()

opposingteam = []
kinpu = ""
while kinpu == "":
    weather = getWeather()

    # Get Opponents pokemon
    curropponent = browser.find_element(By.XPATH,
        "/html/body/div[4]/div[1]/div/div[6]/div[2]/strong").text.split(" ")

    name = curropponent[0]
    level = int(curropponent[1].replace("L", ""))

    # Calculate Stats of Opposing pokemon
    enemystats = helpers.getbasestats(name)
    enemystats[0] = helpers.calculateHP(enemystats[0], level)
    for k in range(1, 6):
        enemystats[k] = helpers.calculateStat(enemystats[k], level)

    enemy = dict()
    enemy["name"] = name
    enemy["stats"] = enemystats
    enemy["level"] = level
    enemy["active"] = True
    enemy["moves"] = helpers.getPossibleMoves(enemy)

    opposingteam.append(enemy.copy())
    print(enemy)

    # Calculate the Damage that your moves do to opposing pokemon
    yourteam = helpers.getYourTeamInfo()
    helpers.yourTeamDamageOpponentPercent(yourteam, enemy, weather)
    print("\n\n\n")
    kinpu = input("Press enter to continue: ")

# Display Data

quit()
