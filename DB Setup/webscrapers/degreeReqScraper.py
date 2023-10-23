import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

majorList = []
requirementDict = {}

def getReqs(i):
    majors[i].click()

    if(i == 40 or i == 41):
        programRequirements = driver.find_element(By.XPATH, '/html/body/div[4]/div[2]/div[2]/nav/ul/li[2]/a')
        programRequirements.click()

    majorList.append(driver.find_element(By.CLASS_NAME, 'page-title').text)
    classes = driver.find_elements(By.CSS_SELECTOR, 'tbody > tr')
    classesStr = {}
    category = []
    classList = []
    for j in range(len(classes)):
        if(classes[j].text != ""):
            splitClass = classes[j].text.split(" ")
            if(splitClass[1].split("\n")[0].isdigit() and int(splitClass[1].split("\n")[0]) > 99 and int(splitClass[1].split("\n")[0]) < 1000):
                classList.append(splitClass[0] + " " + splitClass[1].split("\n")[0])
            elif(splitClass[0] == "or"):
                classList[-1] = classList[-1] + " " + splitClass[0] + " " + splitClass[1] + " " + splitClass[2]
            elif(splitClass[0] == 'Select' or splitClass[0] == "See" or list(splitClass[2])[0] == "I"):
                classList.append(" ".join(splitClass[0 : -1]))
            else:
                if(category != []):
                    classesStr[category] =  classList
                    classList = []
                category = classes[j].text

    requirementDict[majorList[-1]] = classesStr

    driver.back()
    if(i == 40 or i == 41):
        driver.back()
    
driver = webdriver.Chrome()
driver.get("https://bulletin.iit.edu/undergraduate/undergraduate-education/undergraduate-degree-programs/") 

pageContent = driver.find_element(By.CLASS_NAME, 'page_content')
majors = pageContent.find_elements(By.CSS_SELECTOR, "ul > li > a")
for i in range(len(majors)):
    if(i == 39 or i == 40 or i == 41):
        getReqs(i)

outputFileName = "DB Setup/data/majorRequirements.json" 
with open(outputFileName, 'w') as json_file:  
        json_string = json.dump(requirementDict, json_file, indent = 4)