from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
from webdriver_manager.firefox import GeckoDriverManager
import time

password = 'RobotRobot'
username = 'zoybot'

#Loads the Website Data
def loadWebsite(name):
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    browser.get(name)
    # time.sleep(2)
    #
    # # login
    # loginbox = browser.find_element_by_xpath("/html/body/div[1]/div[3]/button[1]")
    # loginbox.click()
    #
    # userbox = browser.find_element_by_name("username")
    # userbox.send_keys(username)
    # userbox.send_keys(Keys.ENTER)
    #
    # time.sleep(.25)
    #
    # passwordbox = browser.find_element_by_name("password")
    # passwordbox.send_keys(password)
    # passwordbox.send_keys(Keys.ENTER)
    #
    input("Press Enter to continue...")

    a = input("next?")
    while(a != 0):
        if(a < 5):
            data = getData(option)
            processed = process(data)
            a = input("data has been processed")
        else:
            printfunc(a)

def getData(option):
    if(option == 1):
        return op1()
    elif(option == 2):
        return op2()
    elif(option == 3):
        return op3()
    elif(option == 4):
        return op4()
    else:
        return op5()

#Each of these methods should return some sort of data structure TBD

#Getting Data of your team initially
def op1(browser, dataframe):
    team = team()
    for k in range(6):
        poke = bottomExtract(browser)
        team[k] = poke
    dataframe.yourTeam = team
    return dataframe

#Getting Data of your opponents pokemon
def op2(browser):
    curopponent = oppExtract(browser)
    dataframe.currOpponent = curopponent
    return dataframe

#Getting Data of the miscellaneous items
def op3(browser):
    whole = browser.find_element_by_xpath('/html')
    htmldata = whole.get_attribute("innerHTML")
    html = str(htmldata)
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.prettify()
    soupstring = str(soup)

    # lines = soupstring.split("\n")
    # for k in range(0, len(lines)):
    #     if '<div class=\"weather\">' in lines[k]:
    #         if '<em>' in lines[k+3] and '</em>' in lines[k+4]:
    #             return "none"
    #         else:
    #             m = k + 1
    #             while "<" in lines[m]:
    #                 m = m + 1
    #             return lines[m].strip()

#Updating data about your pokemon
def op4(browser, dataframe):
    poke = bottomExtract(browser)
    dataframe.yourTeam.replace(poke)
    return dataframe

#Updating data about an oponent pokemon
def op5(browser, dataframe):
    poke = oppExtractSmall(browser)
    dataframe.oppTeam.replace(poke)
    return dataframe

#Print Functions
def printfunc(a):
    if(a == 1):
        p1()
    elif(a==2):
        p2()
    elif(a==3):
        p3()
    else:
        p4()

#Print the damage that current pokemon does to opponent
def p1(data):

#Print the damage that all your pokemon do to opponent
def p2(data):

#Print the damage that all your pokemon do to all opponent pokemo
def p3(data):

#Print the damage the your pokemon x does to the opponents pokemon y
def p4(data, x, y):

loadWebsite('https://play.pokemonshowdown.com/')
