import httplib2
from urllib.parse import urlencode
import json
import jsonpickle
import pickle
import re
import time
from selenium import webdriver



import requests
from bs4 import BeautifulSoup

from Client.models import Bill


def createBill(u,a,b,c,d,e,f,g,k,l,m,i):
    h = httplib2.Http(".cache")

    url = "http://localhost:8000/listBills/"
    bill = Bill({"bill_pk": u,"bill_number":a, "bill_title":b, "chamber_intro":c,
                       "summary":d, "chief_patron": e, "district":f, "house_patrons":g, "senate_patrons":k, "fulltext_i":l, "fulltext_p":m, "session":i})

    bill_json = bill.toJSON()


    body = bill_json
    headers={"content-type":"application/json"}
    resp,content = h.request(uri=url, method="POST", body=body, headers=headers)
    print (resp.status)
    print(bill_json)
    print (content.decode('utf-8'))


if __name__ == '__main__':



    HOST = "localhost"
    USERNAME = "scraper"
    PASSWORD = ""
    DATABASE = "scraping_sample"
    url_list = []
    # ex) for 2020 HB1 - HB500
    #DB20_HB_1_500
    session_year = input("Last two digits of a year:")
    print(session_year)
    bill_type = input("Bill_Type: ex)'HB'").upper()
    print(bill_type)
    range_from = input("Range_From:")
    print(range_from)
    range_end = input("Range_End:")
    print(range_end)
    '''
    #####################################################################################################
    file1 = open(session_year + "_"+ bill_type+"_"+range_from+"_"+range_end+".txt","w",encoding="utf-8")
    #####################################################################################################
    '''
    for k in range(int(range_from), int(range_end)+1):
        #1
        url_to_scrape = "https://lis.virginia.gov/cgi-bin/legp604.exe?"+session_year+"1+sum+"+bill_type+str(k)
        url_list.append(url_to_scrape)


    for url_to_scrape in url_list:

        plain_html_text = requests.get(url_to_scrape)

        # This code is the one that we are having a trouble with
        # We were trying to change the "html.parser" to lxml but we got an
        # error
        soup = BeautifulSoup(plain_html_text.text, "html.parser")
        fulltext_i= "Null"
        fulltext_p= "Null"


        #Bill
        bill_text = soup.find("h3", {"class": "topLine"})
        bill_info = bill_text.text.strip().split()
        #**Bill Number**
        bill_number = bill_info[0]+bill_info[1]
        #**Bill Title**
        bill_title=""
        bill_info_length = len(bill_info)
        for i in range(2,bill_info_length):
            if i == bill_info_length:
                bill_title += bill_info[i]
            else:
                bill_title += bill_info[i]+" "
        if bill_title.strip() != "Budget Bill.":

            #Fulltext
            #Intro

            fulltext_url = soup.find("ul", {"class":"linkSect"})
            fulltext_tags = fulltext_url.find_all('a')
            time.sleep(0.9)
            fulltext_intro = "https://lis.virginia.gov" + fulltext_tags[0].get('href')
            time.sleep(0.9)
            plain_html_text1 = requests.get(fulltext_intro)
            ftxt_intro = BeautifulSoup(plain_html_text1.text, "html.parser")
            text1 = ftxt_intro.find("div", {"id":"mainC"})
            text1.ul.decompose()
            fulltext_i = text1.text

            #Passed

            temp = fulltext_url.find_all('li')
            if len(temp) > 1:
                fulltext_passed = fulltext_intro+"ER"
                plain_html_text2 = requests.get(fulltext_passed)
                ftxt_passed = BeautifulSoup(plain_html_text2.text, "html.parser")
                if ftxt_passed.find("div", {"id":"mainC"}) != None:
                    text2 = ftxt_passed.find("div", {"id":"mainC"})
                    text2.ul.decompose()
                    fulltext_p = text2.text
        '''
        #Governor
        if len(fulltext_tags) > 1:
            fulltext_gg = fulltext_url.find_all("li")
            fulltext_gg = fulltext_gg[-1].text.split(" ")
            fulltext_gg = fulltext_gg[1]
            if fulltext_gg.strip() == "Governor:":
                fulltext_govern = "https://lis.virginia.gov" +fulltext_tags[-1].get('href').replace("pdf", "")
                plain_html_text2 = requests.get(fulltext_govern.replace("pdf", ""))
                ftxt_govern = BeautifulSoup(plain_html_text2.text, "html.parser")
                text2 = ftxt_govern.find("div", {"id":"mainC"})
                text2.ul.decompose()
                fulltext_g = text2.text
                time.sleep(0.9)
        '''



        #**Intro**
        chamber_intro = ""
        if bill_info[0] == "HB":
            chamber_intro = "House of Delegates Bills"
        elif bill_info[0] == "HR":
            chamber_intro = "House of Delegates Resolutions"
        elif bill_info[0] == "HJ":
            chamber_intro = "House of Delegates Joints"
        elif bill_info[0] == "SB":
            chamber_intro = "Senate Bills"
        elif bill_info[0] == "SR":
            chamber_intro = "Senate Resolutions"
        elif bill_info[0] == "SJ":
            chamber_intro = "Senate Joints"

        #session
        session = soup.find("h2")
        #**Session**
        session_info = session.text.strip()
        session_info = session_info[0:4]

        #Chief
        sectMarg = soup.find('p', {"class": "sectMarg"})
        chief_info = sectMarg.text.split("|")
        chief_info = chief_info[0].split("\n")
        #**Chief**
        chief_info = chief_info[1].strip()

        time.sleep(0.9)
        #Summary
        summary_url = url_to_scrape + "S"
        plain_html_text = requests.get(summary_url)
        summary_soup = BeautifulSoup(plain_html_text.text, "html.parser")
        #**All summary types
        summary_head = summary_soup.findAll("h4")
        #**Summary contents
        summary_p = summary_soup.findAll("p")



        all_summary=""
        for i in range (3,len(summary_head)):
            all_summary = all_summary + summary_head[i].text.strip()+"\n"+summary_p[i-1].text.strip().replace("\n"," ") +"\n"

        time.sleep(0.9)
        #sublinks
        district = soup.find('p',attrs={"class":"sectMarg"})
        links = []
        for link in district.findAll('a', attrs={'href': re.compile("")}):
            links.append(link.get('href'))

        time.sleep(0.9)
        #District_URL
        district_url = "https://lis.virginia.gov/" + links[0]
        #District)
        driver = webdriver.Chrome("/Users/slee/Downloads/chromedriver")
        driver.get(district_url)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        #**District**
        district_info="none"
        if soup.find("h3",{"class":"subttl"}) != None:
            if len(soup.find("h3").text.split("-")) > 2:
                district_info = soup.find("h3").text.split("-")[2].strip()
            else:
                district_info = soup.find("h3").text.split("-")[1].strip()

        time.sleep(0.9)
        #All_Patrons_URL
        patrons_url = "https://lis.virginia.gov/" + links[1]
        #Patrons
        plain_html_text = requests.get(patrons_url)
        soup = BeautifulSoup(plain_html_text.text, "html.parser")
        #**Patrons**
        #ex) soup.find("div", {"id": "articlebody"})
        #House Patrons
        hpatron=""
        spatron=""
        if soup.find("div",{"class": "lColLt"}) != None:
            all_hpatron = soup.find("div",{"class": "lColLt"}).text.strip().split("\n")
            for i in range(1,len(all_hpatron)):
                if (i == len(all_hpatron)-1):
                    hpatron = hpatron +(all_hpatron[i])
                else:
                    hpatron = hpatron +(all_hpatron[i])+",\n"
        #Senate Patrons


        if soup.find("div",{"class": "lColRt"}) != None:
            all_spatron = soup.find("div",{"class": "lColRt"}).text.strip().split("\n")
            for i in range(1,len(all_spatron)):
                if (i == len(all_spatron)-1):
                    spatron = spatron +(all_spatron[i])
                else:
                    spatron = spatron +(all_spatron[i])+",\n"

        all_summary2 = all_summary.replace("\n"," ").replace("\r"," ")
        hpatron2 = hpatron.replace("\n"," ")
        spatron2 = spatron.replace("\n"," ")
        fulltext_i2 = fulltext_i.replace("\n"," ").replace("\r"," ")
        fulltext_p2 = fulltext_p.replace("\n"," ").replace("\r"," ")
        time.sleep(0.9)
        bill_pk = session_info+"-"+bill_number
        createBill(bill_pk, bill_number, bill_title, chamber_intro, all_summary2, chief_info, district_info, hpatron2, spatron2, fulltext_i2, fulltext_p2, session_info)
        print(bill_number+"..")
        '''
    #################################################################
        file1.write("Session:"+session_info+"\n")
        file1.write("\nBill_Number: "+bill_number+"\n")
        file1.write("\nBill_Title: "+bill_title+"\n")
        file1.write("\nAll_Summary:\n"+all_summary+"\n")
        file1.write("Chief_Info: "+chief_info+"\n")
        file1.write("\nDistrict_Info: "+district_info+"\n")
        file1.write("\nHouse_Patron:\n"+hpatron+"\n")
        file1.write("\nSenate_Patron:\n"+spatron+"\n")
        file1.write("\n Fulltext:\n\nIntroduced:\n"+fulltext_i+"\n")
        file1.write("\nPassed:\n"+fulltext_p+"\n")
        file1.write("________________________________________________________\n\n")
    file1.close()
    print("File saved")
    ###################################################################
    '''
    print("Finished")




