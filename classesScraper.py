import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

#list of all classes, each in JSON format
class_list = [] 

#choose the subject at index i and open that webpage
def choose_subject(i):
# Second PAGE #
    #Select a Subject
    selectSubject = Select(driver.find_elements(By.NAME, 'sel_subj')[1])
    selectSubject.deselect_all()
    selectSubject.select_by_index(i)

    #Click Submit
    classSearch = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    classSearch.click()

#get each of the classes from that webpage into seperate JSON strings
#append each class to the whole class list
#return to previous webpage
def get_data():
# THIRD PAGE #
    #Get all of the Sections
    ddTitle = driver.find_elements(By.CLASS_NAME, 'ddtitle')
    mainGroup = driver.find_element(By.XPATH, "/html/body/div[3]/table[1]/tbody")
    children = mainGroup.find_elements(By.CSS_SELECTOR, "div > table > tbody > tr > td.dddefault")
    ddDefault = driver.find_elements(By.CLASS_NAME, 'dddefault')
    
    for p in range(len(ddTitle)):
        list = ddTitle[p].text.split(" - ") # title, CRN, (sID, cID), sNum
        
        #Sometimes theres an extra first element, if so, remove it
        if(len(list) == 5):
            list.pop(0)
        
        info = children[p].text.split("\n")
        
        if(info[0][0:15] != "Associated Term"):
            info.pop(0)
        if(info[5].split(" ")[-1] != "Campus"):
            info.insert(3, "Filler Line")

#ERRORS
        if(info[0][0:15] != "Associated Term"):
            print("\nERROR A: " + list[1] + ", " + list[2] + ", " +  info[0])

        if(info[5].split(" ")[-1] != "Campus"):
            print("\nERROR B: " + list[1] + ", " + list[2] + ", " +  info[5])

        if(info[7].split(" ")[-1] != "Method"):
            print("\nERROR C: " + list[1] + ", " + list[2] + ", " +  info[7])
#ERRORS
        #Gets the semester ("Spring", "Summer" or "Fall")
        sem = info[0].split(" ")[2] 

        list.append(info[0].split(" ")[2] + " " + info[0].split(" ")[3]) #term
        list.append(info[5].split(" ")[0]) #campus
         #online  -- Needs to no longer be boolean (Non Traditional, Online, Traditional)
        if(info[7].split(" ")[0] == "Non"):
            list.append(info[7].split(" ")[0] + " " + info[7].split(" ")[1])
        else:
            list.append(info[7].split(" ")[0])
            
        table = children[p].find_elements(By.CSS_SELECTOR, "td.dddefault")

        for i in range (1, 7):
            #(startTime, endTime), days, (building, room), (startDate, endDate), cType, instructors
            #startTime, endTime, days, building, room, startDate, endDate, cType, instructor(s)

            if(i == 1 or i == 4):
                if(table[i].text == "TBA"):
                    list.append("TBA")
                    list.append("TBA")
                else:
                    times = table[i].text.split(" - ")
                    s = "".join(times[0:-1])
                    list.append(s) #startTime/startDate
                    list.append(times[-1]) #endTime/endDate
            elif(i == 3):
                if(table[i].text == "TBA"):
                    list.append("TBA")
                    list.append("TBA")
                else:
                    loc = table[i].text.split(" ")
                    list.append(" ".join(loc[0:-1])) 
                    list.append(loc[-1])   
            else:
                list.append(table[i].text) 

        #Splits sID and cID
        IDSplit = list[2].split(" ")
        
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
            "building": list[10],
            "room": list[11],
            "startDate": list[12],
            "endDate": list[13],
            "cType": list[14],
            "instructors": list[15].split(", ")
        }

        class_list.append(jsonStr)
    returnToPrev = driver.find_element(By.XPATH, '/html/body/div[3]/table[2]/tbody/tr/td/a')
    returnToPrev.click()

    #time.sleep(1)   

def to_JSON():
    #create a .json file from all of the classes
    outputFileName = "Fall_2023.json"
    with open(outputFileName, 'w') as json_file:  
        json_string = json.dump(class_list, json_file, indent = 4)

#Open Chrome
driver = webdriver.Chrome()
driver.get("https://ssb.iit.edu/bnrprd/bwckschd.p_disp_dyn_sched") 

    # FIRST PAGE #
#Select the term of classes
searchForTerm = Select(driver.find_element(By.NAME, 'p_term'))
searchForTerm.select_by_index(1) #First Term In the Dropdown

#Click Submit
submit = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
submit.click()

#Find the dropdown
select = driver.find_elements(By.NAME, 'sel_subj')[1]

#Look through all of the elements in the dropdown (every subject)
for i in range (len(select.find_elements(By.CSS_SELECTOR, '*'))):
    choose_subject(i)
    get_data()

to_JSON()

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