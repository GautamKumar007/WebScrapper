from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time
import argparse

# Setting up argparser
parser = argparse.ArgumentParser(description='StyleSheet')
parser.add_argument('-s', '--service', metavar='', type=str, required=True, help='Service/Stylist/Sallon')
parser.add_argument('-l', '--location', metavar='', type=str, required=True, help='Location where you want your Service/Stylist/Sallon')
arg = parser.parse_args()

# Setting up proxy
Proxy = "163.172.226.142:3838"
options = webdriver.ChromeOptions()
options.add_argument('--proxy-server=%s' % Proxy)


# Setting up Chrome Driver
#PATH = "C:\Program Files (x86)\chromedriver.exe"
#driver = webdriver.Chrome(PATH)
driver = webdriver.Chrome(options=options, executable_path='C:\Program Files (x86)\chromedriver.exe')
driver.get("https://www.styleseat.com/m/")

# Waiting for site to load
driver.implicitly_wait(5)

# Enter Service
search = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/header/responsive-topbar-react/div/div/div/div[1]/div[3]/div/section/div/header/section/input')
search.send_keys(arg.service)
time.sleep(1)
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/header/responsive-topbar-react/div/div/div/div[1]/div[3]/div/section/div/header/section/button[2]').click()

# Search for location
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/react-search-page/div/header/section[2]/section[3]/button/span').click()
s2 = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/react-search-page/div/header/section[2]/section[3]/div/div[2]/div/div/header/span[2]/input')
time.sleep(0.5)

# Clearing location bar
s2.send_keys(Keys.CONTROL, "a", Keys.DELETE)
time.sleep(1)

# Enter location
s2.send_keys(arg.location)
time.sleep(2)
driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div/div/react-search-page/div/header/section[2]/section[3]/div/div[2]/div/div/header/span[2]/button').click()
time.sleep(1)

# Checking if any Services provider exist or not
try:
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-result-content')))
except:
    print('There is no %s at %s' % (arg.service, arg.location))
    driver.close()

#Scroll Down till end
x, y = 0, 0
scroll = driver.find_elements_by_class_name('search-result-body')
x = len(scroll)
while x != y:
    x=y
    driver.execute_script("arguments[0].scrollIntoView();", scroll[-1])
    time.sleep(1)
    scroll = driver.find_elements_by_class_name('search-result-body')
    y = len(scroll)

# All iteams
main = driver.find_elements_by_class_name('search-result-body')
print('There are Total of %s Shops' % len(main))

item_list, count = [], 0

for i in range(len(main)):

    try:
        # Wait for the element to load first
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "search-result-content")))
    except:
        print("Sorry couldn't find specified class name")
        break

    item = driver.find_elements_by_class_name('search-result-body')[i]

    # Important Stuff
    try:
        first_name = item.find_element_by_class_name('first-name').text
    except:
        first_name = ''
    try:
        last_name = item.find_element_by_class_name('last-name').text
    except:
        last_name = ''
    try:
        shop_name = item.find_element_by_tag_name('h3').text
    except:
        shop_name = ''
    try:
        service_name = item.find_element_by_class_name('service-name').text
    except:
        service_name = ''
    try:
        service_duration = item.find_element_by_class_name('service-duration').text
    except:
        service_duration = ''
    try:
        price = item.find_element_by_class_name('service-price').text
    except:
        price = ''
    try:
        rating = item.find_element_by_class_name('average-rating').text
    except:
        rating = ''
    try:
        num_rating = item.find_element_by_class_name('num-ratings').text[1:-1]
    except:
        num_rating = ''
    try:
        links = item.find_element_by_class_name('pro-name').get_property('href')
    except:
        links = ''

    # For Address and Contact which is inside the pro-name
    item.click()
    try:
        # Wait for the next element to load
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div[4]/react-sidebar-info/div/div[2]/div")))
    except:
        print("couldn't find above xpath")
        break

    try:
        add = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div[4]/react-sidebar-info/div/div[2]/div/a/div').text
        add = " , ".join(add.splitlines())
    except:
        add = ''
    try:
        contact = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[1]/div[1]/div[1]/div[4]/react-sidebar-info/div/div[2]/div/div').text
    except:
        contact = ''

    driver.back()

    dict = {'F_name':first_name, 'L_name':last_name, 'Price':price, 'Shop_name':shop_name, 'Service_name':service_name, 'Service_duration':service_duration, 'Contact':contact, 'Address':add, 'Rating':rating, 'Num_rating':num_rating, 'Links':links}
    count += 1
    item_list.append(dict)

    print('Count till now is - %s' % count)
    print(dict)

driver.close()

df = pd.DataFrame(item_list)
print(df)

# Putting Data into csv
df.to_csv('stylsheets(barbers).csv')

