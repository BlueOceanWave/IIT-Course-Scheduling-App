import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

#path = "C:/Users/marci/Desktop/School/chromedriver.exe"


driver = webdriver.Chrome()
driver.get("https://ssb.iit.edu/bnrprd/bwckschd.p_disp_dyn_sched")
    # FIRST PAGE #
#Select the term of classes
searchForTerm = Select(driver.find_element(By.NAME, 'p_term'))
searchForTerm.select_by_index(1)

#Click Submit
submit = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
submit.click()

    # Second PAGE #
#Choose a Subject
selectSubject = Select(driver.find_elements(By.NAME, 'sel_subj')[1])
selectSubject.select_by_index(11)

#Click Submit
classSearch = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
classSearch.click()

    # THIRD PAGE #

time.sleep(10)
'''
course_list = []
for p in range(len(courses)):
    print(courses[p].text)
    course_list.append(courses[p].text)
'''
driver.close