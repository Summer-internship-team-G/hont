from selenium import webdriver


driver = webdriver.Chrome('/Users/yeeun/Downloads/chromedriver')
driver.implicitly_wait(1)
driver.get('https://www.bodybuilding.com/exercises/finder')



# while True:
#     try:
#         btn_more = driver.find_element_by_css_selector(
#            "button.bb-flat-btn.bb-flat-btn--size-lg.js-ex-loadMore.ExLoadMore-btn")
#         btn_more.click()
#         time.sleep(1)
#     except:
#         break

exercise_name = driver.find_elements_by_css_selector('.ExHeading.ExResult-resultsHeading a')
cnt = 1
for content in exercise_name:
    print(cnt, " : ", content.text)
    cnt = cnt+1
print()

muscle_Targeted = driver.find_elements_by_css_selector('.ExResult-details.ExResult-muscleTargeted a')
cnt = 1
for content in muscle_Targeted:
    print(cnt, " : ", content.text)
    cnt = cnt+1
print()

equipment = driver.find_elements_by_css_selector('.ExResult-details.ExResult-equipmentType a')
cnt = 1
for content in equipment:
    print(cnt, " : ", content.text)
    cnt = cnt+1
print()

imgs = driver.find_elements_by_css_selector('img.ExImg.ExResult-img')
cnt = 1
for img in imgs:
    print(cnt, " : ", img.get_attribute('src'))
    cnt = cnt+1
print()
