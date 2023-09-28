import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

class_list = [] 
def choose_subject(i):
    # Second PAGE #
    #Choose a Subject
    selectSubject = Select(driver.find_elements(By.NAME, 'sel_subj')[1])
    selectSubject.deselect_all()
    selectSubject.select_by_index(i)

    #Click Submit
    classSearch = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    classSearch.click()

def get_data():
    # THIRD PAGE #
#Get all of the Sections
    ddTitle = driver.find_elements(By.CLASS_NAME, 'ddtitle')
    ddDefault = driver.find_elements(By.CLASS_NAME, 'dddefault')

    
    for p in range(len(ddTitle)):
        list = ddTitle[p].text.split(" - ") # Title, CRN, (sID, cID), sNum
        if(len(list) == 5):
            list.pop(0)
        info = ddDefault[0].text.split("\n")
        
        infoEx = info[1].split(" ")[2]
        if(infoEx == "Fall" or infoEx == "Spring" or infoEx == "Summer"):
            n = 1
        else: 
            n = 0
        list.append(info[n].split(" ")[2] + " " + info[n].split(" ")[3]) #term
        list.append(info[n + 5].split(" ")[0]) #campus
        list.append(info[n + 7].split(" ")[0]) #online
        for i in range (2, 8):
            #startTime, endTime, days, building, room, startDate, endDate, cType, instructor(s)
            if(i == 2 or i == 5):
                times = ddDefault[i + (p * 8)].text.split(" - ")
                s = "".join(times[0:-1])
                list.append(s) 
                list.append(times[-1]) 
            elif(i == 4):
                loc = ddDefault[i + (p * 8)].text.split(" ")
                list.append(" ".join(loc[0:-1])) 
                if(loc[0] != "TBA"):
                    list.append(loc[-1])   
            else:
                list.append(ddDefault[i + (p * 8)].text) 

        IDSplit = list[2].split(" ")
        print(IDSplit)
        if(len(list) == 16):
            daysEmpty = 1
        else:
            daysEmpty = 0

        jsonStr = { 
            "title": list[0],
            "CRN": list[1],
            "sID":IDSplit[0],
            "cID": IDSplit[1],
            "sNum": list[3],
            "term": list[4],
            "campus": list[5],
            "online": list[6],
            "startTime": list[7],
            "endTime": list[8],
            "days": list[9],
            "building": list[9 + daysEmpty],
            "room": list[10 + daysEmpty],
            "startDate": list[11 + daysEmpty],
            "endDate": list[12 + daysEmpty],
            "cType": list[13 + daysEmpty],
            "instructors": list[14 + daysEmpty].split(", ")
        }
            
        class_list.append(jsonStr)
    returnToPrev = driver.find_element(By.XPATH, '/html/body/div[3]/table[2]/tbody/tr/td/a')
    returnToPrev.click()

    #time.sleep(1)   

#Open Chrome
driver = webdriver.Chrome()
driver.get("https://ssb.iit.edu/bnrprd/bwckschd.p_disp_dyn_sched") 

    # FIRST PAGE #
#Select the term of classes
searchForTerm = Select(driver.find_element(By.NAME, 'p_term'))
searchForTerm.select_by_index(1)

#Click Submit
submit = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
submit.click()

#Find the dropdown
select = driver.find_elements(By.NAME, 'sel_subj')[1]

#Look through all of the elements in the dropdown (every subject)
for i in range (len(select.find_elements(By.CSS_SELECTOR, '*'))):
    #choose the subject at index i and open that webpage
    choose_subject(i)
    #get each of the classes from that webpage into seperate JSON strings
    #append each class to the whole class list
    #return to previous webpage
    get_data()

#create a .json file from all of the classes
outputFileName = "Fall_2023.json"
with open(outputFileName, 'w') as json_file:  
    json_string = json.dump(class_list, json_file, indent = 4)

'''
JSON:
(term.json)
[
    {
        "title": ---
        "CRN": ---
        "sID": ---
        "cID": ---
        "sNum": ---
        "term": --- ???
        "campus": --- ???
        "online": --- ???
        "startTime": --- 
        "endTime": ---
        "days": ---
        "building": ---
        "room": ---
        "startDate": ---
        "endDate": ---
        "cType": ---
        "instructors": [
            name: ---
            ]
    },
    {...
    }
]
'''