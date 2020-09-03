from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time 
import requests
import json
import urllib
import os
import pandas as pd
from glob import glob
from collections import ChainMap
from tqdm.notebook import tqdm as tqdm_notebook
from datetime import datetime 


# Google Chrome Driver Setup
def chromeSetup():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-infobars")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")
 
    return options


def get_selected_cols_df(df, cols):
    '''
    cols : list of str 
    '''
    return df[cols]

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def transform(text):
    try:
        data = pd.to_datetime(text)
        return data.day
    except:
        return text     


def get_Drivers(options, json_path = ".\\config.json",webdriver_path = "C:\\Users\\marco.wang\\Downloads\\chromedriver_win32\\chromedriver"):

    with open(json_path) as f:
        data = json.load(f)

    browers = webdriver.Chrome(webdriver_path,options=options)

    print("get browsers!!")
    log_in_url = 'http://tms.us.lge.com/tm/framework/Frame.jsp'
    browers.get(log_in_url)
    time.sleep(3)
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(3)
    browers.switch_to.frame('resultFrame')


    user = browers.find_element_by_name("loginUser")
    user.send_keys(data['user'])
    password = browers.find_element_by_name("dspLoginPassword")
    password.send_keys(data['password'])
    print("log in !!")

    button = browers.find_element_by_id("buttonEmphasized")
    button.click()


    time.sleep(3)
    browers.switch_to.default_content()
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(3)
    browers.switch_to.frame('nav')

    
    browers.switch_to.default_content()
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(3)
    browers.switch_to.frame('nav')
    IOD = browers.find_element_by_xpath("//*[@id='TREECELL_navigation_18']/a")
    IOD.click()
    time.sleep(3)

    daily = browers.find_element_by_xpath("//*[@id='TREECELL_navigation_18_1']/a[2]")
    daily.click()

    browers.switch_to.default_content()
    time.sleep(0.3)
    browers.switch_to.frame('i2ui_shell_content')
    time.sleep(20)
    browers.switch_to.frame('resultFrame')
    time.sleep(0.3)
    row = 8
    while row < 20:
        total = browers.find_element_by_id(f"iodMonitoringDailyGrid_BODY_{row}_2")
        print(total.text)
        if total.text == "Total":
            print(total.text)
            break
        else: 
            row += 1
    total = browers.find_element_by_xpath(f"//*[@id='iodMonitoringDailyGrid_BODY_{row}_3']/span/a")
    time.sleep(30)
    total.click()
    print("Done!!")
    return browers



def encode_search_word(text):
    return ",".join(map(str,text))



def enter_sys_value():
    return datetime.now().strftime("%m/%d/%Y") + str(datetime.now())[10:16]



def update_iod_tms_with_now(browers):
    i = 0 
    while browers.find_element_by_id(f"iodMonitoringDetailGrid_BODY_{i}_CHECKBOX"):
        checkButton = browers.find_element_by_id(f"iodMonitoringDetailGrid_BODY_{i}_CHECKBOX")
        time.sleep(0.1)
        checkButton.click()
        time.sleep(0.2)
        enter = browers.find_element_by_id(f'iodMonitoringDetailGrid_BODY_{i}_20_INPUT')
        enter.click()
        time.sleep(0.1)
        enter.send_keys(enter_sys_value())
        remark = browers.find_element_by_id(f'iodMonitoringDetailGrid_BODY_{i}_21_INPUT')
        remark.send_keys(datetime.now().strftime("%m/%d/%Y") + "Marco")
        i += 1
        if i > 30:
            browers.find_element_by_tag_name('body').send_keys(Keys.END)