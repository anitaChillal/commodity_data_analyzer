import datetime

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as WW
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains as AC
from random import randint
from time import sleep
import pdb
import re
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from bs4 import Comment
from pymongo import MongoClient
from selenium.webdriver import ActionChains



location = ['Kolkata', 'Pune' , 'Bangalore' , 'Mumbai', 'Delhi','Chennai']

def refresh(driver):
    try:
        driver.find_element_by_tag_name('div')
    except BrokenPipeError:
        pass


def city_based_onion_scraper(city):
    price_obj = {}
    display = Display(visible=0, size=(1840,690))
    display.start()
    browser2 = webdriver.Firefox()
    browser2.maximize_window()
    browser2.get('https://www.bigbasket.com')
    browser2.find_element_by_xpath("//*[@class='btn hvr-fade']").click()

    form = browser2.find_element_by_xpath("//*[@class='dropdown new-to-bb xhrcalls-only drop-z-index open']")\
        .find_element_by_xpath("//*[@class='dropdown-menu latest-at-bb']")\
        .find_element_by_xpath("//*[@class='ng-pristine ng-valid-editable ng-invalid ng-invalid-required']")

    el = form.find_element_by_xpath("//*[@class='form-group area-autocomplete city-select']")\
        .find_element_by_xpath("//*[@class='ui-select-container ui-select-bootstrap dropdown ng-pristine ng-untouched ng-valid ng-scope ng-not-empty']")\
        .find_element_by_xpath("//*[@class='ui-select-match ng-scope']")\
        .find_element_by_xpath("//*[@class='btn btn-default form-control ui-select-toggle']")

    el.click()

    sleep(randint(3,5))

    refresh(browser2)

    el2 = form.find_element_by_xpath("//*[@class='form-group area-autocomplete city-select']")\
        .find_element_by_xpath("//*[@class='ui-select-container ui-select-bootstrap dropdown ng-pristine ng-untouched ng-valid ng-scope ng-not-empty open']")\
        .find_element_by_tag_name('input')
    el2.send_keys(city,Keys.RETURN)

    el3 = form.find_element_by_xpath("//*[@class='skp-exp']")\
        .find_element_by_xpath("//*[@class='btn btn-default ng-scope']")

    el3.click()

    sleep(10)

    refresh(browser2)

    submit_element = WW(browser2,100).until(EC.visibility_of_element_located((By.XPATH, "//*[@class='btn btn-default bb-search']")))

    el4 = browser2.find_element_by_id('headerControllerId')\
        .find_element_by_xpath("//*[@class='bb-brand-section ng-scope']")\
        .find_element_by_xpath("//*[@class='col-md-6 col-sm-12 col-xs-12 mb-pad-0 mb-zindex search-bar']")\
        .find_element_by_xpath("//*[@class='input-group']")

    input_element = el4.find_element(By.XPATH, "//*[@class='form-control ng-pristine ng-untouched ng-valid ng-empty']")
    input_element.send_keys('onion',Keys.RETURN)
    submit_element.click()

    sleep(15)
    refresh(browser2)

    raw_onion_soup = BeautifulSoup(browser2.page_source,'html.parser')
    [x.extract() for x in raw_onion_soup.find_all('script')]
    [x.extract() for x in raw_onion_soup.find_all('style')]
    [x.extract() for x in raw_onion_soup.find_all('meta')]
    [x.extract() for x in raw_onion_soup.find_all('noscript')]
    [x.extract() for x in raw_onion_soup.find_all(text=lambda text:isinstance(text, Comment))]
    html = raw_onion_soup.contents
    for i in html:
       #print (i)
        html = raw_onion_soup.prettify("utf-8")
    file_name = "{}_onion_output.html".format(city.lower())
    with open(file_name, "wb") as file:
        file.write(html)

    product_divs = raw_onion_soup.find_all('div',{'class' : "item prod-deck row ng-scope"})
    for div in product_divs:
        product_name=div.find_next('div' , {'qa' : 'product_name'}).find_next('a').text
        if product_name == 'Onion' or product_name == 'Onion - Medium/Kanda- Madhyam' or product_name == 'Onion - Medium/Vengayam' :

            price_lis = div.find_next('ul',{'class' : "dropdown-menu drop-select"}).find_all('li',{"ng-repeat":"allProducts in product.all_prods "})
            #pdb.set_trace()
            for price_li in price_lis:
                if re.compile('1 kg').match(price_li.find('span',{'ng-bind':'allProducts.w'}).text):
                    price = float(price_li.find('span',{'ng-bind':'allProducts.sp'}).text)
                    price_obj = dict([('location',city),('price', price)])
                    # print(price_obj)
                    break
                else:
                    continue

            break
        else:
            continue

    # print(price_obj)
    browser2.quit()
    display.stop()
    return price_obj

def main():
    final_price_obj_list = []
    try:
        for loc in location:
            final_price_obj_list.append(city_based_onion_scraper(loc))
        print(final_price_obj_list)
    #    block for mongodb operations #
        try:
            conn = MongoClient()
            print("Connected successfully!!!")

        except:
            print("Could not connect to MongoDB")
            pass
        # database
        db = conn.commodity_db

        # Created or Switched to collection names: bigbasket_location_onion
        collection = db.bigbasket_location_onion
        now = datetime.datetime.now()
        date_creation=now.strftime("%Y-%m-%d %H:%M")

        # Insert Data
        for d in final_price_obj_list:
            rec_id1 = collection.insert_one({"creation_date": date_creation,"mrp":d['price'],"location":d['location']})


    except Exception as e:
        print(e)
        pass

if __name__ == '__main__' :
    main()






