import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from bs4 import BeautifulSoup
from bs4 import Comment
from pymongo import MongoClient



def main():
    display = Display(visible=0, size=(800, 600))
    display.start()
    browser = webdriver.Chrome()
    browser.get('https://www.bigbasket.com/pd/10000148/fresho-onion-1-kg/')
    soup1 = BeautifulSoup(browser.page_source, 'html.parser')
    [x.extract() for x in soup1.find_all('script')]
    [x.extract() for x in soup1.find_all('style')]
    [x.extract() for x in soup1.find_all('meta')]
    [x.extract() for x in soup1.find_all('noscript')]
    [x.extract() for x in soup1.find_all(text=lambda text:isinstance(text, Comment))]
    html =soup1.contents
    for i in html:
       #print (i)
        html = soup1.prettify("utf-8")
    with open("output_selenium.html", "wb") as file:
        file.write(html)
    product = soup1.find(class_="sc-Rmtcm gzZYfK")
    price_string=product.string
    price=float(price_string[8:13])
    print(price)

    #print(browser.title)
    browser.quit()
    display.stop()


    # Python code to illustrate
    # inserting data in MongoDB

    try:
        conn = MongoClient()
        print("Connected successfully!!!")

    except:
        print("Could not connect to MongoDB")

    # database
    db = conn.commodity_db

    # Created or Switched to collection names: my_gfg_collection
    collection = db.bigbasket
    now = datetime.datetime.now()
    date_creation=now.strftime("%Y-%m-%d %H:%M")

    # Insert Data
    rec_id1 = collection.insert_one({"creation_date": date_creation,"mrp":price})

    print("Data inserted ",rec_id1)

    # Printing the data inserted
    #cursor = collection.find()
    #for record in cursor:
     #   print(record)


if __name__ == '__main__':
    main()




