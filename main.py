import json
import os
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


Alphabetarr = ['A', 'B','C','D','E', 'F','G', 'H', 'I', 'J', 'K', 'L','M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for letter in Alphabetarr:
    
    Itemcount = 0
    link = 'https://luenersv-judo.de/index.php/vereinsinfo/wissenswertes/woerterbuch/' + letter + '?start='\
           + str(Itemcount)
    driver = webdriver.Chrome(executable_path='C:\\Users\\teraf\\chromedriver_win32\\chromedriver.exe')
    driver.get(link)
    GridItems = driver.find_elements(by=By.CLASS_NAME, value='span4')
    filename = "C:\\Users\\teraf\\OneDrive\\Desktop\\Judo Begriff Lexikon\\" + letter + ".json"
    FileStart = {"Metadata_" + letter: []}
    RunningThroughChar = True
    
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(FileStart, file, indent=0)
        
    while RunningThroughChar:
        if len(GridItems) == 0:
            RunningThroughChar = False
            driver.close()
            
        for Item in GridItems:
            Itemcount += 1
            Title_Item = Item.find_element_by_class_name('title')
            Text_Item = Item.find_element_by_class_name('text').find_element_by_class_name('line_limit')
            Title_Text = Title_Item.find_element_by_tag_name('a').get_attribute('innerHTML')
            Text_Text = Text_Item.get_attribute('innerHTML')
            if Text_Text.__contains__('span'):
                SpanElements = Text_Item.find_elements_by_tag_name('span')
                for Element in SpanElements:
                    ZuSchreibenderText = Element.get_attribute('innerHTML')
                    if Element.get_attribute('innerHTML').__contains__('<a'):
                        ZuSchreibenderText = Element.find_element_by_tag_name('a').get_attribute('innerHTML')
                    ZuErsetzenderText = '<span>' + Element.get_attribute('innerHTML') + '</span>'
                    Text_Text = Text_Text.replace(ZuErsetzenderText, ZuSchreibenderText,1)
                    
            Text_Text = Text_Text.replace('<p>', '').replace('</p>', '').replace('<br>', ' ')
            Text_Text = Text_Text.replace('??', 'oe').replace('??', 'ue').replace('??', 'ae')

            JSON = {
                "Japanese" : Title_Text,
                "German" : Text_Text
            }
            with open(filename, 'r+', encoding='utf-8') as file:
                # First we load existing data into a dict.
                file_data = json.load(file)
                # Join new_data with file_data inside emp_details
                file_data["German"].append(JSON)
                # Sets file's current position at offset.
                file.seek(0)
                # convert back to json.
                json.dump(file_data, file, indent=0)
            if Itemcount % 15 == 0 and len(GridItems) == 15:
                link = 'https://luenersv-judo.de/index.php/vereinsinfo/wissenswertes/woerterbuch/' + letter + '?start='\
                       + str(Itemcount)
                driver.get(link)
                GridItems = driver.find_elements(by=By.CLASS_NAME , value='span4')
            if len(GridItems) < 15 and len(GridItems) == Itemcount % 15:
                RunningThroughChar = False
                driver.close()


