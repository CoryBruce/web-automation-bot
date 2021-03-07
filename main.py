import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox(executable_path=r"C:\Users\coryb\PycharmProjects\geckodriver.exe")



def get_weather(zipcode):
    driver.get('https://www.weather.gov/')
    search_bar = driver.find_element_by_id("inputstring")
    del_char = 18
    while del_char > 0:
        search_bar.send_keys(Keys.BACK_SPACE)
        del_char -= 1
    search_bar.send_keys(zipcode)
    time.sleep(2)
    search_bar.send_keys(Keys.ARROW_DOWN)
    search_bar.send_keys(Keys.RETURN)
    try:
        current_weather = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'current-conditions-body'))
        )

        print(current_weather.text)
    except:
        driver.quit()


    #print(driver.page_source)
    forcast = driver.find_element_by_id('detailed-forecast')
    driver.quit()
    print(forcast.text)


get_weather(64507)