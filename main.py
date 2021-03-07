import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox(executable_path=r"C:\Users\coryb\PycharmProjects\geckodriver.exe")



def get_weather_data(zipcode):
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
            EC.presence_of_element_located((By.ID, 'current-conditions-body')))
        current_weather_text = current_weather.text
    except:
        driver.quit()
    forcast = driver.find_element_by_id('detailed-forecast')
    forcast_text = forcast.text
    driver.quit()
    return current_weather_text, forcast_text

def get_weather():
    current_weather, forecast = get_weather_data(64507)
    current_weather_trim = current_weather.split('\n')
    forecast_trim = forecast.split('\n')
    weather = []
    weather.append('Current Weather: ')
    weather.append(current_weather_trim[8])
    weather.append(current_weather_trim[0])
    weather.append(current_weather_trim[1])
    weather.append(current_weather_trim[3])
    count = 1
    while count < 13:
        weather.append(forecast_trim[count])
        count += 1
    return weather

def display_weather():
    weather = get_weather()

    for item in weather:
        print(item)
        #print('\n')


display_weather()