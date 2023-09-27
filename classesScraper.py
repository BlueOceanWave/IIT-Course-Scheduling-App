import time
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
        info = ddDefault[0].text.split("\n")
        list.append(info[1].split(" ")[2] + " " + info[1].split(" ")[3]) #term
        list.append(info[6].split(" ")[0]) #campus
        list.append(info[8].split(" ")[0]) #online
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
        if(p == 0):
            print(list)
        class_list.append(list)
    returnToPrev = driver.find_element(By.XPATH, '/html/body/div[3]/table[2]/tbody/tr/td/a')
    returnToPrev.click()

    #time.sleep(1)   


driver = webdriver.Chrome()
driver.get("https://ssb.iit.edu/bnrprd/bwckschd.p_disp_dyn_sched")
    # FIRST PAGE #
#Select the term of classes
searchForTerm = Select(driver.find_element(By.NAME, 'p_term'))
searchForTerm.select_by_index(1)

#Click Submit
submit = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
submit.click()

select = driver.find_elements(By.NAME, 'sel_subj')[1]
for i in range (len(select.find_elements(By.CSS_SELECTOR, '*'))):
    print(i)
    choose_subject(i)
    get_data()
