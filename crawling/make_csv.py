from selenium import webdriver
import pandas as pd
import time

driver = webdriver.Chrome('/Users/yeeun/Downloads/chromedriver')
driver.implicitly_wait(1)
driver.get('https://www.bodybuilding.com/exercises/finder')


#15장
page = 0
while page < 15:
    # try:
    btn_more = driver.find_element_by_css_selector("button.bb-flat-btn.bb-flat-btn--size-lg.js-ex-loadMore.ExLoadMore-btn")
    btn_more.click()
    page += 1
    time.sleep(1)

    # except:
    #     break

exercise_name = driver.find_elements_by_css_selector('.ExHeading.ExResult-resultsHeading a')
muscle_Targeted = driver.find_elements_by_css_selector('.ExResult-details.ExResult-muscleTargeted a')
equipment = driver.find_elements_by_css_selector('.ExResult-details.ExResult-equipmentType a')
imgs = driver.find_elements_by_css_selector('img.ExImg.ExResult-img')

name_list = []
m_list = []
e_list = []
i_list = []

for i in exercise_name:
    name_list.append(i.text.split('\n'))
for j in muscle_Targeted:
    m_list.append(j.text.split('\n'))
for k in equipment:
    e_list.append(k.text.split('\n'))
for l in imgs:
    i_list.append(l.get_attribute('src').split('\n'))

data = pd.DataFrame({'exercise name':name_list, 'muscle':m_list, 'equipment':e_list, 'imgs':i_list})
data.to_csv('result.csv')
