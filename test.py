from selenium import webdriver
import time

login = ''
passw=''

all=10

browser=webdriver.Chrome(r"D:\pyt\chromedriver.exe")
# browser.get("https://www.instagram.com/")

browser.get("https://www.instagram.com/accounts/login")
time.sleep(2)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[2]/div/label/input").send_keys(login)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[3]/div/label/input").send_keys(passw)
browser.find_element_by_xpath("//section/main/div/article/div/div[1]/div/form/div[4]/button").click()
time.sleep(2)

browser.get("https://www.instagram.com/bestofvegan/")
time.sleep(2)
browser.find_element_by_xpath("//section/main/div/header/section/ul/li[2]/a").click()
time.sleep(2)
element=browser.find_element_by_xpath("/html/body/div[4]/div/div[2]")

browser.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight/%s" %6,element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight/%s" %4,element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight/%s" %3,element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight/%s" %2,element)
time.sleep(0.8)
browser.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight/%s" %1.4,element)
time.sleep(0.8)

pers=[] #users array
t=2 #waiting
num_scroll=0
p=0

while len(pers)<all:
    num_scroll+=1
    browser.execute_script("arguments[0].scrollTop=arguments[0].scrollHeight",element)


    if num_scroll%10==0:
        print('!')
       
        persons=browser.find_elements_by_xpath("//div[@role='dialog']/div[2]/ul/div/li/div/div/div/div/a[@title]")
        print('persons',persons)
        # persons=browser.find_element_by_xpath("/html/body/div[4]/div/div[2]/ul/div/li[1]/div/div[2]/div[1]/div/div/a")
        for i in range(len(persons)):
            pers.append(str(persons[i].get_attribute('href')))
        # print('pers',pers)
    
    time.sleep(t)
    if(len(pers)>(1000+1000*p)):
        print('\nWaiting 10 min...')
        time.sleep(60*10)
        p+=1

f=open(r"D:\pyt\test.txt", 'w')
for person in pers:
    f.write(person)
    f.write('\n')
f.close()

browser.quit()