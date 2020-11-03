#!/usr/bin/env python3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorthief import ColorThief
import webcolors
import urllib
import urllib.request
import time




def getField(id):
    """
    Returns the name of product item for given link

    Args:
        link (string) represents link of item for title to be retreived from.
        id (string) represents id field to be returned.
    Returns:
        field (string) represents string of item for given id.
    """

    try:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, id)))
        title = driver.find_element_by_id(id)
        return title.text
    except:
        print("Could not find ID: ", id)
        return None

def getColor(photoTitle):
    """
    Returns the color most prominent in item image.

    Args:
        photoTitle (string) represents photoTitle to predict color of.
    Returns:
        color (string) represents color of item for given photo.
    """

    color_thief = ColorThief(photoTitle)
    c = color_thief.get_color(quality=1)

    min_colours = {}
    print(c)
    for key, name in webcolors.css21_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - c[0]) ** 2
        gd = (g_c - c[1]) ** 2
        bd = (b_c - c[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return (min_colours[min(min_colours.keys())])

def getImages():
    """
    Compiles item images into directory
    """

    #Arbitrary 10 photos to be taken
    for i in range(10):
        #Ebay only has 3 images per carosel page, so need to go to next
        if ((i + 1) % 3 == 0):
            driver.find_element_by_xpath('//*[@id="vi_main_img_fs_slider"]/a[2]').click()
        #Save photo if there is one
        try:
            driver.find_element_by_xpath('//*[@id="vi_main_img_fs_thImg' + str(i) + '"]/table/tbody/tr/td/div/img').click()
            img = driver.find_element_by_xpath('//*[@id="icImg"]')
            src = img.get_attribute('src')
            urllib.request.urlretrieve(src, "im" + str(i) + ".png")
        except:
            print("Error capturing image.")




def postToGrailed():
    """
    Posts item to grailed, currently only able to get to sign in and stuck at captcha
    """
    # name, price, category, designer, size, color
    time.sleep(.2)
    driver.find_element_by_xpath('//*[@id="global-header-login-btn"]').click()
    time.sleep(.2)
    driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div/div/button[4]').click()
    time.sleep(.2)
    driver.find_element_by_xpath('//*[@id="email"]').send_keys('username')
    time.sleep(.2)
    driver.find_element_by_xpath('//*[@id="password"]').send_keys('password')
    time.sleep(.2)
    driver.find_element_by_xpath('/html/body/div[7]/div/div/div/div[2]/div/div/form/button').click()






#Example link
link = "https://www.ebay.com/itm/Vintage-90s-The-Nature-Company-T-Shirt-Animal-Wildlife-Tee-Men-s-Medium-Stitch-L/124125750097?_trkparms=aid%3D1110012%26algo%3DSPLICE.SOIPOST%26ao%3D1%26asc%3D229890%26meid%3D36556672778a46ab91d45e1971a8d780%26pid%3D100008%26rk%3D4%26rkt%3D12%26sd%3D124040422087%26itm%3D124125750097%26pmt%3D1%26noa%3D0%26pg%3D2047675%26algv%3DPromotedSellersOtherItemsV2&_trksid=p2047675.c100008.m2219"
driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(link)


#initializing eBay information
name = getField("itemTitle")
price = getField("prcIsum")
category = getField("vi-VR-brumb-lnkLst").split()[-1]
designer = ("Vintage")
description = ("Fantastic vintage piece. Appears as shown in images. Please contact with any questions!")
size = ("Medium")
getImages()
color = getColor('im1.png')


print("Name: " + name)
print("Price: " + str(price))
print("Category: " + category)
print("Designer: " + designer)
print("Size: " + size)
print("Color: " + color)


#posting Grailed information
driver.get('https://www.grailed.com/users/sign_up')
postToGrailed()


driver.quit()
