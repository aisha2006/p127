from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome(executable_path="./chromedriver.exe")
browser.get(START_URL)
time.sleep(10)

headers = ["V Mag. (mV)","Proper name","Bayer designation","Distance (ly)","Spectral class"	,"Mass (M☉)","Radius (R☉)","Luminosity (L☉)"]
star_data = []
new_star_data = []

def scrape():
    for i in range(0, 457): 
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul in soup.find_all("ul", attrs={"class", "noprint"}):
            li_tags = ul.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index==0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            star_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a')
        print(f"{i} page done 1")

def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")

        new_star_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

scrape()
for index, data in enumerate(star_data):
    #Taking index number of hyperlink from star_data
    scrape_more_data(data[5])    
    print(f"{index+1} page done 2")


final_star_data = []
for index, data in enumerate(star_data):
    new_star_item = new_star_data[index] 
    new_star_item = [elem.replace("\n","") for elem in new_star_item]
    new_star_item = new_star_item[:7]
    final_star_data.append(data+new_star_item)

with open("final.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(final_star_data)



