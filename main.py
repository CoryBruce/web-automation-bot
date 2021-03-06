from bs4 import BeautifulSoup
from tkinter import *
import re
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def write_job_data(list):
    with open('job_web_data', 'w')as f:
        for item in list:
            f.write(str(item))

def organize_job_data(page_source_list):
    job_list = []
    for page in page_source_list:
        soup = BeautifulSoup(page, features='html.parser')
        divs = soup.find_all('div', class_='jobsearch-SerpJobCard')
        for item in divs:
            title = item.find('a').text.strip()
            company = item.find('span', class_='company').text.strip()
            try:  # use try except block cause not every job has this field so if none then pay = ''
                pay = item.find('span', class_='salaryText').text.strip()
            except:
                pay = 'not posted'
            job_summary = item.find('div', {'class': "summary"}).text.strip().replace('\n',
                                                                                      '')  # this replaces the \n in the text with ''
            job_link = item.find('a', href=True)
            link = 'indeed.com' + job_link['href']
            try:
                remote = item.find('span', {'class': "remote"}).text.strip()
            except:
                remote = 'not displaying remote'
            try:
                location = item.find('div', class_='location accessible-contrast-color-location').text.strip()
            except:
                location = 'no info'
            try:
                rating = item.find('span', class_="ratingsContent").text.strip()
            except:
                rating = 'no rating'
            job = {
                'title': title,
                'company': company,
                'rating': rating,
                'pay': pay,
                'location': location,
                'summary': job_summary,
                'remote': remote,
                'link': link}
            job_list.append(job)
    return job_list

def grab_job_page_sources():
    data = load_data()
    zipcode = data[2]
    job_titles = data[3].split(',')
    driver = webdriver.Firefox(executable_path=r"C:\Users\coryb\PycharmProjects\geckodriver.exe")
    #driver.minimize_window()
    page_sources = []

    for i in range(len(job_titles)):
        driver.get('https://www.indeed.com/')
        job_search = driver.find_element_by_id('text-input-what')
        job_search.send_keys(job_titles[i])
        area_search = driver.find_element_by_id('text-input-where')
        del_char = 20
        while del_char > 0:
            area_search.send_keys(Keys.BACK_SPACE)
            del_char -= 1
        area_search.send_keys(zipcode)
        time.sleep(1)
        area_search.send_keys(Keys.RETURN)
        time.sleep(4)

        new_url = '&fromage=3'
        url = driver.current_url + new_url
        driver.get(url)
        time.sleep(2)
        try:
            driver.find_element_by_xpath('//*[@id="popover-email"]').send_keys('test@gmail.com')
            driver.find_element_by_xpath('//*[@id="job-alert-popover-button"]').click()
            driver.find_element_by_xpath('/html/body/div[4]/div[1]/button').click()
        except:pass
        try:
            page_count = driver.find_element_by_class_name('pagination')
            page_list = str(page_count.text).split('\n')
            page = (len(page_list) - 1) * 10
            new_page_url = f'&start={10}'
            url = driver.current_url + new_page_url
            driver.get(url)
            time.sleep(5)
        except:pass
        time.sleep(2)
        page_source = driver.page_source
        page_sources.append(page_source)

    jobs = organize_job_data(page_sources)
    return jobs

def return_jobs():
    jobs = grab_job_page_sources()
    for job in jobs:
        print(job)

def grab_weather_data(zipcode):
    driver = webdriver.Firefox(executable_path=r"C:\Users\coryb\PycharmProjects\geckodriver.exe")
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

def organize_data(zipcode):
    current_weather, forecast = grab_weather_data(zipcode)
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

def weather(zipcode):
    weather = organize_data(zipcode)
    with open('weather.text','w') as f:
        for item in weather:
            f.write(item)
            f.write('\n')
            #print(item)
    return weather

def grab_stock_data():
    driver = webdriver.Firefox(executable_path=r"C:\Users\coryb\PycharmProjects\geckodriver.exe")
    driver.get('https://finance.yahoo.com/')
    top_gains = driver.find_element_by_id('data-util-col')
    time.sleep(3)
    driver.quit()
    return top_gains

def organize_stock_data():
    data = grab_stock_data()
    return data

def stocks():
    stocks = organize_stock_data()
    print(stocks.text)

def new_user():
    def write_txtfile(list):
        with open('data.txt', 'w') as f:
            data = list
            for item in data:
                f.write(item)
                f.write('\n')
    def write_data():
        user = username_entry.get()
        pass1 = password_entry.get()
        pass2 = password_entry2.get()
        zip = zipcode_entry.get()
        job_list = job_titles.get()
        #jobs = str(job_list).split(',')
        print(job_list)
        if pass1 == pass2:
            print(f'Created new user {user}')
            print('Saving data...')
            list = [user, pass1, zip, job_list]
            write_txtfile(list)
            root.destroy()
        else:
            print('Passwords dont match!')

    root = Tk()
    root.title('Login')
    canvas = Canvas(root, width=100, height=500)
    canvas.grid(columnspan=5, rowspan=11)
    title = Label(canvas, text="Personal Butler", width=15, font=('bold', 25))
    title.grid(column=1)
    header = Label(canvas, text="Create Account", font=('bold', 14))
    header.grid(column=1, row=1)
    space = Canvas(canvas, width=100, height=50)
    space.grid(column=0, row=2)
    username_label = Label(canvas, text="Enter Username: ", font=('bold', 10))
    username_label.grid(column=0, row=3)
    username_entry = Entry(canvas)
    username_entry.grid(column=1, row=3)
    small_space = Canvas(canvas, width=60, height=15)
    small_space.grid(column=3, row=4)
    password_label = Label(canvas, text="Enter Password: ", font=("bold", 10))
    password_label.grid(column=0, row=5)
    password_entry = Entry(canvas)
    password_entry.grid(column=1, row=5)
    password_entry2 = Entry(canvas)
    password_entry2.grid(column=1, row=6)
    small_space2 = Canvas(canvas, width=100, height=15)
    small_space2.grid(column=0, row=7)
    zipcode = Label(canvas, text="Enter Zipcode: ", font=('bold', 10))
    zipcode.grid(column=0, row=8)
    zipcode_entry = Entry(canvas)
    zipcode_entry.grid(column=1, row=8)
    job_titles_label = Label(canvas, text='Enter job titles and separate with (",") :', font=('bold', 10))
    job_titles_label.grid(column=0, row=9)
    job_titles = Entry(canvas)
    job_titles.grid(column=1, row=9)
    small_space3 = Canvas(canvas, width=100, height=25)
    small_space3.grid(column=0, row=10)
    submit = Button(canvas, text='Submit', relief=GROOVE, font=('arial', 12, 'bold'), command=write_data)
    submit.grid(column=1, row=11)
    root.mainloop()

def load_data():
    with open('data.txt', 'r') as f:
        data = f.read()
        new_data = data.split('\n')
        # print(new_data[0])
        return new_data

def login_gui():
    def print_info():
        userr = username_entry.get()
        pwdd = password_entry.get()
        print(userr, pwdd)

    def check_login():
        data = load_data()
        user1 = username_entry.get()
        pass1 = password_entry.get()
        if user1 == data[0]:
            if pass1 == data[1]:
                print('Login successful')
                root.destroy()
                main_menu()
            else:
                print('Wrong password')
        else:
            print('No username in system')

    user = StringVar
    pwd = StringVar
    root = Tk()
    root.geometry('500x500')
    root.title('Login')
    title = Label(root, text="Personal Butler", width=25, font=('bold', 25))
    title.place(x=30, y=20)
    header = Label(root, text="Please login", width=20, font=('bold', 14))
    header.place(x=60, y=270)
    username_label = Label(root, text="Username: ", width=20, font=('bold', 10))
    username_label.place(x=80, y=330)
    username_entry = Entry(root, textvar=user)
    username_entry.place(x=240, y=330)
    password_label = Label(root, text="Password: ", width=20, font=("bold", 10))
    password_label.place(x=80, y=380)
    password_entry = Entry(root, textvar=pwd)
    password_entry.place(x=240, y=380)
    submit = Button(root, text='Submit', relief=GROOVE, font=('arial', 12, 'bold'), command=check_login)
    submit.place(x=240, y=420)

    root.mainloop()

def main_menu():
    def search_jobs():
        return_jobs()

    def display_weather():
        def clean_up_now():
            now = datetime.now()
            list = str(now).split(' ')
            raw_time = list[1]
            time_list = raw_time.split(':')
            time = time_list[0]
            return time
        def check_days(): #check the days from time stamp data against the current day and return true if same day
            now = datetime.now()
            list = str(now).split(' ')
            raw_date = list[0]
            date_list = raw_date.split('-')
            date1 = date_list[2]
            try:
                date = date1.strip('0')
            except:
                date = date1
            return date

        def check_time():
            with open('weather.text', 'r') as f:
                data = f.read()
                data_list = data.split('\n')
                try:
                    timestamp_raw = data_list[1]
                    #timestamp = timestamp_raw.strip("Last update")
                    #timestamp = timestamp.strip("pm CST")
                    timestamp = timestamp_raw.split(' ')
                    day = timestamp[2]
                    month = timestamp[3]
                    #print(timestamp)
                    if timestamp[5] == 'pm':
                        print('pm')
                        raw_time = timestamp[4]
                        if len(raw_time) == 4:# need to check the min and round hours up or down accordingly
                            time = (int(raw_time[0])*100) + 1300
                        if len(raw_time) == 5:
                            h1 = int(raw_time[0])*1000
                            h2 = (int(raw_time[1])*100) + 200
                            time = h1 + h2
                    if timestamp[5] == 'am':
                        print('am')
                        raw_time = timestamp[4]
                        if len(raw_time) == 4:
                            time = raw_time[0] * 100
                        if len(raw_time) == 5:
                            h1 = raw_time[0]*1000
                            h2 = raw_time[1]*100
                            time = h1 + h2
                except:
                    time = 0000

                now_days = check_days()
                if day < now_days:
                    return True
                    pass
                #print(time)
                now_hour = clean_up_now()
                now_hour = int(now_hour) * 100
                #print(now)
                dif = now_hour - int(time)
                #print(dif)
                if dif > 30:
                    return True

        need_weather_update = check_time()
        current_weather = ''
        if need_weather_update:
            print('Updating weather')
            weather_data = weather(zip)
            i = 0
            while i < 5:
                line = weather_data[i] + '\n'
                current_weather += line
                i += 1
            need_weather_update = False
        else:
            weather_data = []
            with open('weather.text', 'r') as f:
                raw_data = f.read()
                weather_data = raw_data.split('\n')
                i = 0
                while i < 5:
                    line = weather_data[i] + '\n'
                    current_weather += line
                    i += 1

        print(current_weather)
        text = Text(canvas, height=5, width=30)
        text.insert(END, current_weather)
        text.grid(column=1, row=4)
    data = load_data()
    user = data[0]
    zip = data[2]
    root = Tk()
    root.title('Personal Butler')
    canvas = Canvas(root, width=100, height=500)
    canvas.grid(columnspan=5, rowspan=5)
    title = Label(canvas, text=f"Welcome {user}", width=15, font=('bold', 25))
    title.grid(column=1)
    header = Label(canvas, text="App stuff goes here", font=('bold', 14))
    header.grid(column=1, row=1)
    weather_btn = Button(canvas, text="Weather", relief=GROOVE, font=('arial', 12, 'bold'), command=display_weather)
    weather_btn.grid(column=1, row=5)
    job_btn = Button(canvas, text="Job Search", relief=GROOVE, font=('arial', 10), command=search_jobs)
    job_btn.grid(column=2, row=5)
    root.mainloop()





#main_menu()# delete this after testing

with open('data.txt', 'r') as f:
    data = f.read()
    #print(len(data))
    if len(data)<= 0:
        new_user()
        login_gui()
    else:
        login_gui()

#stocks()