from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import random
random.seed()

login = 'crucified_none'
passw='v1FfA9a9'

like_time=10
all_likes=10
all_subsc=10
like_per_hour=10
subs_per_hour=10

likes=0
subscs=0

def xpath_ex(url):
    try:
        browser.find_element_by_xpath(url)
        existence=1
    except NoSuchElementException:
        existence=0
    return existence

browser=webdriver.Chrome(r"D:\pyt\chromedriver.exe")

browser.get("https://www.instagram.com/accounts/login")
time.sleep(2)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(login)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(passw)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button").click()
time.sleep(2)

f=open(r"D:\pyt\persons_list.txt", 'r')
file_list=[]
for line in f:
    file_list.append(line)
f.close()

subsc_list=[]
f1=open(r"D:\pyt\my_subscs.txt")
for line in f1:
    subsc_list.append(line)
f1.close()

j=0
n=0
next_pers=0
start_time=time.time()

for person in file_list:
    if likes>=all_likes:
        print('no more likes')
        break
    if subscs>=all_subsc:
        print('no more subsc')
        break
    if ((time.time()-start_time)<=60*60) and (subs_per_hour<=subscs):
        print('no more subsc per hour')
        print('wait...')

        #удалить из списка тех, на кого уже подписались
        f=open(r"D:\pyt\persons_list.txt", 'w')
        for i in range(j, len(file_list)) :
            f.write(file_list[i])
        f.close()
        time.sleep(60*60-(time.time()-start_time))
        start_time=time.time()
        subscs=0
        likes=0

    if ((time.time()-start_time)<=60*60) and (like_per_hour<=likes):
        print('no more likes per hour')
        print('wait...')

        #удалить из списка тех, на кого уже подписались
        f=open(r"D:\pyt\persons_list.txt", 'w')
        for i in range(j, len(file_list)) :
            f.write(file_list[i])
        f.close()
        time.sleep(60*60-(time.time()-start_time))
        start_time=time.time()
        subscs=0
        likes=0

    if(time.time()-start_time)>=60*60:
        start_time=time.time()
        subscs=0
        likes=0


    #сравнение с массивом подписок
    for line in subsc_list:
        next_pers=0
        if person==line:
            next_pers=1
            print(j+1, '\t подписка на Этого чела уже есть')
            j+=1
            n+=1
            break
    if next_pers==1:
        continue

    j+=1
    print("\n"+str(j-n)+": ")

    browser.get(person)
    time.sleep(1.5)

    #Открытие публикаций и лайкинг

    #проверка есть ли уже подписка на єтого пользователя
    element="//section/main/div/header/section/div[1]/div[1]/span/span[1]/button"
    if xpath_ex(element)==1:
        try:
            follow_status=browser.find_element_by_xpath(element).text
        except StaleElementReferenceException:
            print(j, "error, code: 1")
            continue
        if(follow_status=='Following') or (follow_status=='Подписки'):
            print('you have already followed')
            continue

#поиск и открытие двух случайных публикаций 
    element="//a[contains(@href, '/p/')]"
    if xpath_ex(element)==0:
        print(j, "error, code: 2")
        continue

    posts=browser.find_elements_by_xpath(element)
    i=0
    for post in posts:
        posts[i]=post.get_attribute("href")
        i+=1
    rand_post=random.randint(0,2) #случайній пост от 1 до 6
    for i in range(2):
        browser.get(posts[rand_post+i])
        time.sleep(0.8)

        browser.find_element_by_xpath("//section/main/div/div[1]/article/div[2]/section[1]/span[1]/button").click()
        likes+=1
        print("+1 like")
        time.sleep(like_time)
    
    try:
        element="//section/main/div/div[1]/article/header/div[2]/div[1]/div[2]/button"
        if xpath_ex(element)==0:
            print(j, "error, code 3")
            continue
        try:
            browser.find_element_by_xpath(element).click()
        except StaleElementReferenceException:
            print(j, 'error, code 4')
            continue
    except ElementClickInterceptedException:
        print(j, "error, code 5")
        continue

    subscs+=1
    print("+1 subsc", person[0:len(person)-1])
    time.sleep(0.5)

    f=open(r"D:\pyt\my_subscs.txt", 'a')
    f.write(person)
    f.close()

browser.quit()

