from selenium import webdriver
import time
from datetime import timedelta,datetime
import re

days=100
acc_subscription=1000
publications=2
today=datetime.now()

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

def xpath_ex(url):
    try:
        browser.find_element_by_xpath(url)
        existence=1
    except NoSuchElementException:
        existence=0
    return existence

browser=webdriver.Chrome(r"D:\pyt\chromedriver.exe")

f=open(r"D:\pyt\test.txt", 'r')
file_list=[]
for line in f:
    file_list.append(line)
f.close()

filtered_list=[]
j=0
i=0

for pers in file_list:
    j+=1
    browser.get(pers)
    time.sleep(0.4)

    element="//section/main/div/div/article/div[1]/div/h2"
    if xpath_ex(element)==1:
        try:
            if browser.find_element_by_xpath(element).text=="This Account is Private" or "Это закрытый аккаунт":
                print(j, 'private')
                continue
        except StaleElementReferenceException:
            print(
                'Error, 1')

    element="//section/main/div/header/section/ul/li[3]/a/span"
    if xpath_ex(element)==0:
        print(j, 'error, 2')
        continue
    status=browser.find_element_by_xpath(element).text
    status=re.sub(r'\s', '', status)
    if int(status)>acc_subscription:
        print(j, 'too much subsc')
        continue

    element="//section/main/div/header/section/div[2]/a"
    if xpath_ex(element)==1:
        print(j, 'link in the bio')
        continue

    element="//section/main/div/header/section/ul/li[1]/a/span"
    if xpath_ex(element)==0:
        print(j,'error 3')
        continue
    status=browser.find_element_by_xpath(element).text
    status=re.sub(r'\s','',status)
    if int(status)<publications:
        print(j,'too little publications')
        continue

    element="//section/main/div/header/div/div/span/img"
    if xpath_ex(element)==0:
        print(j, 'error 4')
        continue
    status=browser.find_element_by_xpath(element).get_attribute("src")
    if status.find("s150x150")==1:
        print(j, 'no avatar')
        continue

    element="//a[contains(@href, '/p/')]"
    if xpath_ex(element)==0:
        print(j, 'error 5')
        continue
    status=browser.find_element_by_xpath(element).get_attribute("href")
    browser.get(status)
    post_date=browser.find_element_by_xpath("//time").get_attribute("datetime")
    year=int(post_date[0:4])
    month=int(post_date[5:7])
    day=int(post_date[8:10])
    post_date=datetime(year, month, day)
    period=today-post_date
    if period.days>days:
        print('last publication was more time ago')
        continue

    filtered_list.append(pers)
    print('add new pers', pers)
    i+=1
    if i>10:
        break

f=open(r"D:\pyt\persons_list.txt", 'w')
for line in filtered_list:
    f.write(line)
f.close()  

print(f'add {i} persons')

browser.quit()