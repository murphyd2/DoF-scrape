"""Dylan Murphy 2018-29-18
This program collects the property tax histories of a given BBL"""

from selenium import webdriver
import csv
import re
import time

#https://regex101.com/r/TICehB/3
def Caleb(url,boroughcode,Block,Lot):
    browser = webdriver.Chrome()
    browser.get(url)
    boroughcombo=browser.find_element_by_xpath("/html/body/div/center/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/"
                                                "div/table[3]/tbody/tr/td/div/p/table/tbody/tr/td/table/tbody/tr[2]/td/"
                                                "form/table/tbody/tr[2]/td[2]/select")
    blockentry= browser.find_element_by_xpath("/html/body/div/center/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/"
                                               "div/table[3]/tbody/tr/td/div/p/table/tbody/tr/td/table/tbody/tr[2]/td/"
                                               "form/table/tbody/tr[3]/td[2]/input")
    lotentry= browser.find_element_by_xpath("/html/body/div/center/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/div/"
                                             "table[3]/tbody/tr/td/div/p/table/tbody/tr/td/table/tbody/tr[2]/td/form/"
                                             "table/tbody/tr[4]/td[2]/input")
    submitbtn = browser.find_element_by_xpath("/html/body/div/center/table[2]/tbody/tr/td[1]/table/tbody/tr[2]/td[2]/div/"
                                              "table[3]/tbody/tr/td/div/p/table/tbody/tr/td/table/tbody/tr[2]/td/form/table"
                                              "/tbody/tr[7]/td/input[1]")

    boroughcombo.send_keys(boroughcode)
    blockentry.send_keys(Block)
    lotentry.send_keys(Lot)
    submitbtn.click()

    finalasseslink= browser.find_element_by_xpath("/html/body/div/center/div/center/table[1]/tbody/tr[1]/td[1]/table/"
                                                  "tbody/tr[2]/td[2]/div/table[3]/tbody/tr[2]/td/table/tbody/tr/td[2]/"
                                                  "font/font[2]/b/a")
    finalasseslink.click()

    totalvaluation = browser.find_element_by_xpath(
        "/html/body/div/table[1]/tbody/tr[2]/td/table[9]/tbody/tr[2]/td[3]/font")
    propertytax = browser.find_element_by_xpath(
        "/html/body/div/table[1]/tbody/tr[2]/td/table[12]/tbody/tr[2]/td[2]/font")
    taxclass = browser.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/table[3]/tbody/tr[5]/td[3]/font")
    buildingclass = browser.find_element_by_xpath(
        "/html/body/div/table[1]/tbody/tr[2]/td/table[3]/tbody/tr[6]/td[3]/font")
    year_info= {'current':[totalvaluation.text,propertytax.text,taxclass.text,buildingclass.text]}
    if finalasseslink:
        page = browser.execute_script("return document.body.innerHTML")

        regex =r"href=\"(.+)\">\s*View (\d{4}) FINAL ASSESSMENT"

        test_str = (page)

        subst = ""

        # You can manually specify the number of replacements by changing the 4th argument
        result = re.findall(regex, test_str, re.MULTILINE)
        print(result)
        for i in result:
            a,b,c,d=repeat(browser,i[0])
            year_info[i[1]]=[a,b,c,d]
        with open("{}_{}_{}_property tax history.csv".format('3', '2238', '49'), "w") as f:
            writer = csv.writer(f, dialect="excel")
            fieldnames = list(year_info.keys())
            print(fieldnames)
            print("keys", list(year_info.keys()))
            vallist = list(year_info.values())
            print("items", str(year_info.items()))
            # writer.writerow(str(year_info.items()))
            counter = 0
            years = list(year_info.keys())
            print(years[0])
            for item in years:
                writer.writerow(str(years[counter]))
                for i in range(4):
                    writer.writerow(vallist[i])
                counter += 1

        print(year_info)
def repeat(browser,url):
    browser.get("https://nycprop.nyc.gov/nycproperty/statements/asr/jsp/"+url)
    time.sleep(2)
    totalvaluation = browser.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/table[9]/tbody/tr[2]/td[3]/font")
    propertytax= browser.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/table[12]/tbody/tr[2]/td[2]/font")
    taxclass = browser.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/table[3]/tbody/tr[5]/td[3]/font")
    buildingclass = browser.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/table[3]/tbody/tr[6]/td[3]/font")
    return totalvaluation.text,propertytax.text,taxclass.text,buildingclass.text

def main():
    bbltuple= tuple(input("Enter the borough code (1:MN, 2:Bronx,3:Brooklyn,4:Queens,5:SI), Block and Lot in the format '1,2069,35':").split(','))
    bc,b,l = bbltuple[0],bbltuple[1], bbltuple[2]
    Caleb("https://nycprop.nyc.gov/nycproperty/nynav/jsp/selectbbl.jsp", bc,b,l)
main()