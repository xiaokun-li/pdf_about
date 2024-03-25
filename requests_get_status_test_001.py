# _*_ coding:utf-8 _*_
import requests
import time

def check_tomcat_status(url, interval=10):
    while True:
        try:
            response = requests.get(url, verify=False)
            if response.status_code == 200:
                print(f"Tomcat is running at {url}")
            else:
                print(f"Tomcat is not running or responding incorrectly at {url}. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error connecting to {url}: {e}")

        time.sleep(interval)

    # 使用示例


check_tomcat_status("https://ebusiness.dbschenker.hk.com/", interval=10)