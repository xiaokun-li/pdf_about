# _*_ coding:utf-8 _*_

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests

chromedriver = r"C:\Users\xman\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe"

webchrome = webdriver.Chrome(service=Service(chromedriver))

targeturl = r"https://www.dbschenker.com/app/nges-portal/contract-logistics/contract-logistics-site"
#  https://auth.dbschenker.com
#  https://www.dbschenker.com/app/dashboard/
#  https://www.dbschenker.com/app/nges-portal/contract-logistics/contract-logistics-site
#  https://ebusiness.schenker.com.hk/Portal/hpmcd/invsum.html

res = requests.get(targeturl)

print(res.status_code)

webchrome.get(targeturl)

input("input some text for ending test...")
